from django.shortcuts import render
from django.http import HttpResponse
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

@login_required

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_genres = Genre.objects.count()
    num_books_filter = Book.objects.filter(title__icontains='Half').count()
    num_visits = request.session.get('num_visits',0)
    request.session['num_visits']=num_visits+1
    context = {
        'num_books':num_books,
        'num_instances': num_instances,
        'num_instances_available':num_instances_available,
        'num_authors': num_authors,
        'num_genres' : num_genres,
        'num_books_filtered': num_books_filter,
        'num_visits': num_visits,
    }

    return render(request,'index.html',context=context)
class BookListView(LoginRequiredMixin,generic.ListView):
    model = Book
    template_name = 'book_list.html'
class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book 
    template_name = 'book_detail.html'
class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    template_name = 'author_list.html'
class AuthorDetailview(LoginRequiredMixin, generic.DetailView):
    model = Author
    template_name = 'author_detail.html'
class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')