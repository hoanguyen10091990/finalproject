from django.contrib import admin
from .models import Book, Author, Category, Review, User

# Register your models here.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(User)