import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from django.db.models import Q



from .forms import AuthorForm, NewBookForm, ReviewForm
from .models import Book, Author, Category, User, Review, MyBook


def index(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    categories = Category.objects.all()

    books = Book.objects.filter(Q(category__name__icontains=q) | Q(name__icontains=q)).order_by('-created')
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    reviews = Review.objects.all().order_by('-created')[:10]
    return render(request, "bookreview/index.html", {
        "books": books,
        "categories": categories,
        "reviews": reviews,
        "page_obj": page_obj
    })


def author_profile(request, author_id):
    try:
        author = Author.objects.get(pk=author_id)
        books = author.books.all()
        book_count = books.count()
    except Author.DoesNotExist:
        return HttpResponse("Invalid author access")

    return render(request, "bookreview/author.html", {
        "author": author,
        "books": books,
        "book_count": book_count
    })
        


@login_required(login_url='login')
def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name'].lower()
            try:
                author = Author.objects.get(name=name)
                # Send message
                messages.alert(request, 'Author already exists')
                return HttpResponseRedirect(reverse("add_author"))

            except Author.DoesNotExist:
                about = form.cleaned_data['about']
                nationality = form.cleaned_data['nationality']
                image = request.FILES.get('image', 'no_image.jpg')
                author = Author(name=name, nationality=nationality, about=about, image=image)
                author.save()
                return HttpResponseRedirect(reverse("index"))
        else:
            form = AuthorForm(form)
            return render(request,"bookreview/add_author.html", {
            "form": form
        })

    else:
        form = AuthorForm()
        return render(request,"bookreview/add_author.html", {
            "form": form
        })


@login_required(login_url='login')
def add_book(request):
    if request.method == "POST":
        form = NewBookForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect(reverse("index"))
            except IntegrityError:
                form = NewBookForm(form)
                messages.warning(request, "This book is already exist !!!")
                return HttpResponseRedirect(reverse("add_book"))
               
        else:
            messages.warning(request, "Input value invalid !!!")
            return HttpResponseRedirect(reverse("add_book"))

    else:
        form = NewBookForm()
        return render(request, 'bookreview/add_book.html', {
            "form": form
        })


def book_view(request, book_isbn):
    try:
        book = Book.objects.get(isbn=book_isbn)
        authors = book.author.all()
        reviews = book.reviews.all().order_by("-created")
        book_rating = book.reviews.aggregate(Avg('rating'))['rating__avg']
    except Book.DoesNotExist:
        return HttpResponse("Invalid ISBN")

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Get date from form
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]
            rating = form.cleaned_data["rating"]
            user = User.objects.get(pk=request.user.id)
            review = Review(posted_by=user, book=book, title=title, body=body, rating=rating)
            # Save review
            review.save()
            # Send message
            messages.success(request, 'Review posted successful')
            return HttpResponseRedirect(reverse("book", args=(book_isbn,)))
        else:       
            return HttpResponse("Input invalid")

    else:
        # Check book is added to my Book or not
        try:
            mybook = MyBook.objects.get(book=book, user = User.objects.get(pk=request.user.id))
            is_added = True
        except (MyBook.DoesNotExist, User.DoesNotExist):
            is_added = False          

        return render(request, "bookreview/book.html", {
            "book": book,
            "authors": authors,
            "form": ReviewForm(),
            "reviews": reviews,
            "book_rating": book_rating,
            "is_added": is_added
        })


@csrf_exempt
@login_required(login_url='login')  
def delete(request, review_id):
    # Query for requested review
    try:
        review = Review.objects.get(pk=review_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Review not found."}, status=404)

    # Check review is posted by user or not
    if review.posted_by.id != request.user.id:
        return JsonResponse({
            "error": "Delete invalid"
        }, status=400)

    # Delele review
    if request.method == "PUT":
        review.delete()
        return JsonResponse({"message": "Review delete successfully."}, status=201)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)


@csrf_exempt
@login_required(login_url='login')  
def add_my_book(request, book_isbn):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        book = Book.objects.get(isbn=book_isbn)

        try:
            # Add to my book
            mybook = MyBook(book=book, user=user)
            mybook.save()
            messages.success(request, 'This book was added to your reading list !')
            return HttpResponseRedirect(reverse("book", args=(book_isbn,)))
        except IntegrityError:
            # Remove from my book API
            mybook = MyBook.objects.get(book=book, user=user)
            mybook.delete()
            return JsonResponse({"message": "This book removed successfully"}, status=201)

    else:
        return HttpResponse(405)


@csrf_exempt
@login_required(login_url='login')  
def my_reading(request):
    user = User.objects.get(pk=request.user.id)
    if request.method == "GET":
        # Display my reading page 
        added = user.my_books.all().order_by("-updated")
        books = []

        for item in added:
            book = {"book": item.book, "process": item.process}
            books.append(book)
        
        return render(request, "bookreview/my_reading.html", {
            "books": books
        })
    elif request.method == "PUT":
        # Handle for API request
        data = json.loads(request.body)
        isbn = data.get("isbn")
        process = data.get("process")
        try:
            book = Book.objects.get(isbn=isbn)
        except Book.DoesNotExist:
            return JsonResponse({"error": "Book ISBN not found."}, status=404)
        
        reading = MyBook.objects.get(book=book, user=user)
        reading.process = process
        reading.save()
        return JsonResponse({"message": "Process updated successfully."}, status=201)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "bookreview/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "bookreview/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "bookreview/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "bookreview/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "bookreview/register.html")

