from django.db import models
from django.db.models.base import Model
from django.urls  import  reverse
from django.contrib.auth.models import User
import uuid
from datetime import date

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True,blank=True)
    date_of_death = models.DateField('Died',null=True,blank=True)

    class Meta:
        ordering = ['last_name','first_name']

    def get_absolute_url(self):
        return reverse('author-detail',args=[str(self.id)])

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'

class Genre(models.Model):
    name = models.CharField(max_length=200,help_text="Enter a book genre (eg. Science,Fiction...")

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author',on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000,help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN',max_length=13,unique=True,help_text='13 Character <a href="https://isbn-international.org/content/what-isbn">ISBN Number</a>')
    genre = models.ManyToManyField(Genre,help_text='select a genre for the book')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail',args=[str(self.id)])

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,help_text='Unique ID for this Particular Book across the whole library')
    book = models.ForeignKey('Book',on_delete=models.RESTRICT,null=True)
    imprint = models.CharField(max_length=200,help_text='Imprint Date')
    due_back = models.DateField(null=True,blank=True)

    LOAN_STATUS = (
        ('m', 'Maintainance'),
        ('o', 'On Loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1,choices=LOAN_STATUS,blank=True,default='m',help_text='Book Availability')
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ['due_back']
        permissions = (('can_mark_returned','Set book as returned'),)
    
    def __str__(self):
        return f'{self.id} ({self.book.title})'  

      