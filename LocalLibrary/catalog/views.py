
from django.db import models
from django.http import request
from django.views import generic
from django.shortcuts import render, get_object_or_404
from .models import Author,Book,BookInstance,Genre
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RenewBookForm
import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
# Create your views here.                                               

def index(request):
    num_books = Book.objects.all().count()
    num_authors = Author.objects.count()
    num_instance = BookInstance.objects.all().count()
    num_instance_available = BookInstance.objects.filter(status__exact='a').count()
    total_books_genres = Genre.objects.all().count()
    num_visits = request.session.get('num_visits',0)
    request.session['num_visits'] = num_visits+1

    context = {
        'num_books': num_books,
        'num_authors': num_authors,
        'num_instance': num_instance,
        'num_instance_available': num_instance_available, 
        'genres_total': total_books_genres, 
        'num_visits': num_visits, 
    }

    return render(request,'index.html',context=context)

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'books_list'
    template_name = 'books.html'
    paginate_by = 3

def book_detail_view(request,pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request,'book_info.html',context={'book': book})

class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'authors_list'
    template_name = 'authors.html'
    paginate_by = 10

def author_detail_view(request,pk):
    author = get_object_or_404(Author,pk=pk)
    return render(request,'author_info.html',context={'author': author})

class LoanedBooksByUser(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name = 'books_borrowed_by_user.html'
    paginate_by = 10 
    context_object_name = 'loaned_books'

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance,pk = pk)
    
    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

        return HttpResponseRedirect(reverse('my-borrowed'))

    else:
        
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

        context = {
            'form': form,
            'book_instance': book_instance,
        }

    return render(request, 'renew_book_librarian.html', context)

class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death':'01/01/1738'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__'

class AuthorDelete(DeleteView):
    model = Author
    success_url =  reverse_lazy('authors_page')