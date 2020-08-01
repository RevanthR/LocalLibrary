from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
import datetime
from django.urls import reverse
from catalog.forms import RenewBookForm

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

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

class AllBooksListView(PermissionRequiredMixin,generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'all_books.html'

