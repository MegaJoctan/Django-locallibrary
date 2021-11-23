from os import name
from django.urls import path
from . import urls
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('books/',views.BookListView.as_view(),name='books_page'),
    path('book/<int:pk>/',views.book_detail_view,name='book-detail'),
    path('authors/',views.AuthorListView.as_view(),name='authors_page'),
    path('author/<int:pk>/',views.author_detail_view,name='author-detail'),
    path('author/create/',views.AuthorCreate.as_view(),name='author-create'),
    path('author/<int:pk>/delete/',views.AuthorDelete.as_view(),name='author-delete'),
    path('author/<int:pk>/modify/',views.AuthorUpdate.as_view(),name='author-update'),
    path('mybooks/',views.LoanedBooksByUser.as_view(),name='my-borrowed'),
    path('book/<uuid:pk>/renew/',views.renew_book_librarian,name='renew_book_librarian'),
]