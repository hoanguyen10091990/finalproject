from django.urls import path

from . import views 

urlpatterns = [
    path('', views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_author", views.add_author, name="add_author"),
    path("add_book", views.add_book, name="add_book"),
    path("book/<str:book_isbn>", views.book_view, name="book"),
    path("author_profile/<int:author_id>", views.author_profile, name="author"),
    path("add_reading/<str:book_isbn>", views.add_my_book, name="add_mybook"),
    path("my_reading", views.my_reading, name="my_reading"),
    # API route 
    path("book/delete/<int:review_id>", views.delete, name="delete"),
    path("update_process", views.my_reading, name="update"),
]