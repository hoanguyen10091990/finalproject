from django import forms
from .models import Category, Author, Book, Review



class NewBookForm(forms.ModelForm):
    

    class Meta:
        model = Book
        fields = ["name", "subname", "description", "author", "image", "category", "isbn"]
        labels = {
            "name": "Book name",
            "subname": "Subtitle",
            "description": "Description",
            "author": "Author",
            "image": "Book cover",
            "category": "Category",
            "isbn": "ISBN"
        }
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Name ...",
                "class": "form-control my-2"
                }),
            "subname": forms.TextInput(attrs={
                "placeholder": "Subtitle ...",
                "class": "form-control my-2"
                }),
            "description": forms.Textarea(attrs={
                "placeholder": "About ...",
                "class": "form-control my-2"
                }),
            "isbn": forms.TextInput(attrs={
                "placeholder": "ISBN ...",
                "class": "form-control my-2"
            })
    
        }


class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ["name", "nationality", "about", "image" ]
        labels = {
            "name": "Name ",
            "about": "About ",
            "nationality": "Nationality",
            "image": "Author Image"
        }
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Name name...",
                "class": "form-control my-2"
                }),
            "about": forms.Textarea(attrs={
                "placeholder": "About ...",
                "class": "form-control my-2"
                }),
            "nationality": forms.TextInput(attrs={
                "placeholder": "Input nationality",
                "class": "form-control my-2"
                })
        }


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ["title", "body", "rating"]
        labels = {
            "title": "",
            "body": "",
            "rating": "Rating"
        }

        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Title",
                "class": "form-control my-2"
                }),
            "body": forms.Textarea(attrs={
                "placeholder": "Please input your review",
                "class": "form-control my-2", 
                'cols': '60',
                'rows': '5'
                }),
            "rating": forms.NumberInput(attrs={
                "min": 1,
                "max": 5,  
                "placeholder": "Please input rating from 1 to 5",
                "class": "form-control my-2"
                })
        }
        

