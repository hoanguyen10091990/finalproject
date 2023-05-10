# CS50W - Final project capstone - Bookreview Project


# Introduction
## Description and requirements
My final project is Bookread-liked clone. Users are able to register, post reviews with rating. They can also search book through category or book name by search bar or category side menu in navbar.

The project was built using Django as a backend framework and JavaScript as a frontend programming language. All generated information are saved in database (SQLite by default).

All webpages of the project are mobile-responsive.

All requirements can be viewed here: https://cs50.harvard.edu/web/2020/projects/final/capstone/

You must be registered to use options such as posting review, rating, add book or update reading process. 

## Features

1. Create book and author
2. Reviews book
3. Rates book
4. Views author profile
5. Create my reading list
6. Tracking for reading

* Youtube URL: https://youtu.be/tiLJrzL1ndI

## Distinctiveness and Complexity:
Why this project is distinct from all previous projects ?

  - This project is a bookreview-liked project which is completely distinct from the other projects in this course (Network, mail, commerce ...)
  - Uses JS to fetch API data repeatly without reloading the page.
  - Uses JS to generate stars depend on book rating and all reviews rating.
  - Uses JS to display reading process rangebar interactive with user and update through API.
  - Flexible category-based search and search bar for index page.
  - Setting to upload image for bookcover and author profile.
  - Uses django for back-end and javascript for front-end.
  - Completely Mobile responsive.

## Installation
  - Make and apply migrations by running `python manage.py makemigrations` and `python manage.py migrate`.
  - Create superuser with `python manage.py createsuperuser` to create new category in admin board. This step is optional.
  - Go to website address and register an account.

# Implementation
## Models
### User 
Contains AbstractUser field

### Category
Contains all categories of book.

Fields:
* name - Category names

### Book
Contains all book info.

Fields:
* name - name of book
* subname - subtitle of book
* description - description of this book
* author - author of this book
* category - category of this book
* isbn - isbn of this book (unique)
* image - image of bookcover
* updated - book info 's update date
* created  - book's publication date


### Author 
Contains all author info

Fields:
* name - name of author 
* nationality - nationality of author
* about - info about author
* image - image for author profile


### Review 
Contains all reviews info

Fields:
* posted_by - user who posted review
* book - book which is reviewed for
* title - review's title
* body - review's body
* rating - rating for book
* created - review posted date


### MyBook
Contains all user's reading list info
Fields:
* user - user who add book to reading list
* book - book which is added to reading list
* process - book's reading process
* updated - process's update date
* created - book's added date

## Views
### index
Here you can:
* View all books
* View all category and search book by category
* View all recently comment on books


### add_book 
(only for logged-in users)

Display add new book form for add new book.

### add_author
(only for logged-in users)

Display add new author form for add new author.

### author_profile
Display author_profile and books of this author

### book_view

* Display book info
* Display book rating
* Display all reviews of this book

### book_view
(only for logged-in users)

Add/remove book to your favorite/reading list by render/API.

### my_reading
(only for logged-in users)

* Display all reading list of user.
* Update book reading process of user.

### logout_view
Controls logging out.

### register
Controls registration.

## Static
### JS folder 

There are 3 javascript file:
* book.js - js for book profile page include rating to stars convert function and delete function for fetch API
* quote.js - generate quote for quoteblock of homepage repeatly every 10 seconds
* my_reading.js - js for my reading list page, include process range bar update API and remove book from reading list API

### styles.css 
Contains styling css file for responsive

## Admin.py
Registed for Book, Author, Category, Review, User models

## media
This directory contains one default image (no_image.jpg), and here will be saved all users photos

## urls.py
All application/API URLs.

## admin.py
Setting for admin board.

## templates/bookreview
Contains all template for bookreview apps

---
Special thanks to Brian and the entire CS50 team for this course.