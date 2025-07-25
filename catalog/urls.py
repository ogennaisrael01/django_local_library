from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name="index"),
    path("books/", views.BookListView.as_view(), name="books"),
    path("book/<int:id>/", views.detailview,  name="book_detail"),
    path("authors/", views.list_authors, name="authors"), 
    path("authors/<int:pk>/", views.AuthorDetialView.as_view(), name="author_detail"),
    path('register/', views.registerview, name="register"),
    path("my_books/", views.loaned_book_view, name="my_borrowed_books"),
    path("liberian_view/", views.staff_Loaned_book_view, name="all_borrowed_books")
]