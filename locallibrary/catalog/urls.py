from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('books/',views.BookListView.as_view(), name='books'),
    path('books/<int:pk>',views.BookDetailView.as_view(), name = 'book-detail'),
    path('authors/',views.AuthorListView.as_view(),name='author'),
    path('authors/<int:pk>', views.AuthorDetailview.as_view(),name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

