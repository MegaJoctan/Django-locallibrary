
from django.contrib import admin
from .models import Author,Book,BookInstance,Genre

# Register your models here.
 
admin.site.register(Genre)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','date_of_birth','date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
 
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author','display_genre')  
    inlines = [BookInstanceInline]

    def display_genre(self,obj):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in obj.genre.all()[:3])

    display_genre.short_description = 'Genre'

class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status','due_back')
    list_display = ('book','status','due_back')

    fieldsets = (
        (None,{
            'fields': ('book','imprint','id')
        }),

        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )


# Register Data 

admin.site.register(Author,AuthorAdmin)
admin.site.register(Book,BookAdmin) 
admin.site.register(BookInstance,BookInstanceAdmin)

