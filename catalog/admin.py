from django.contrib import admin
from .models import Book, BookInstance, Author, Language, Genre, CustomUser
# Register your models here.
admin.site.register(Language)
admin.site.register(Genre)

class BookInline(admin.TabularInline):
    model = Book

@admin.register(Author) # the same thing with admin.site.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "date_of_birth", "date_of_death"]
    fields = ["first_name", "last_name", ("date_of_birth", "date_of_death")]
    inlines = [BookInline]

class BookInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "display_genre"]
    inlines = [BookInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ["id", "book", "status", "due_back", "borrower"]
    list_filter = ["status", "due_back"]
    fieldsets = [
        (None, {
            "fields": ["book", "imprint", "id"]
        }),
        ("Availability", {
            "fields": ["status", "due_back", "borrower"]
        })
    ]

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["email", "username", "profile_picture"]
    list_filter = ["username"]
    

