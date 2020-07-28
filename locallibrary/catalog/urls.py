from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('books/',views.BookListView.as_view(), name='books'),
    path('books/<int:pk>',views.BookDetailView.as_view(), name = 'book-detail'),
    path('authors/',views.AuthorListView.as_view(),name='author'),
    path('authors/<int:pk>', views.AuthorDetailview.as_view(),name='author-detail'),
]

