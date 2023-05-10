from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator



class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name 


class Author(models.Model):
    name = models.CharField(max_length=64)
    nationality = models.CharField(max_length=200, blank=True, null=True)
    about = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images/', default='no_image.jpg')

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=200)
    subname = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    author = models.ManyToManyField(Author, related_name="books", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    isbn = models.IntegerField(unique=True)
    image = models.ImageField(upload_to='images/', default='no_image.jpg')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Review(models.Model):

    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="posted")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    title = models.CharField(max_length=200)
    body = models.TextField()
    rating = models.IntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class MyBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_books")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    process = models.IntegerField(
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ],
        default = 0
    )
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'book']

    def __str__(self):
        return f"{self.user}: {self.book}"



