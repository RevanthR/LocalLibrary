from django.shortcuts import render
from django.http import HttpResponse
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
# Create your views here.
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_genres = Genre.objects.count()
    num_books_filter = Book.objects.filter(title__icontains='Half').count()
    context = {
        'num_books':num_books,
        'num_instances': num_instances,
        'num_instances_available':num_instances_available,
        'num_authors': num_authors,
        'num_genres' : num_genres,
        'num_books_filtered': num_books_filter,
    }

    return render(request,'index.html',context=context)
class BookListView(generic.ListView):
    model = Book
    template_name = 'book_list.html'
class BookDetailView(generic.DetailView):
    model = Book 
    template_name = 'book_detail.html'