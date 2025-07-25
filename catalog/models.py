from django.db import models
from django.urls import reverse
from django.db.models.functions import Lower
from django.db.models import UniqueConstraint
from django.contrib.auth.models import AbstractUser
import uuid
from datetime import date 
from django.conf import settings
# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="email address")
    profile_picture = models.ImageField(verbose_name="image", name="profile_picture", null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    REQUIRED_FIELDS = ["username"]
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.get_username()
    
    def get_absolute_url(self):
        return reverse("user_details", args=[str(self.id)])
    

class Genre(models.Model):
    """
        Model representing a book genre
    """
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a book genre (eg,  Science fiction, French Poetry etc,)"

    )

    def __str__(self):
        """ String reperensatation of the model object """
        return self.name
    
    def get_absolute_url(self):
        """ returns a URL to access a particular genre"""
        return reverse("genre_details", args=[str(self.id)])
    
    class Meta:
        """ Constraints for  unique fields"""
        constraints = [
            UniqueConstraint(
                Lower("name"),
                name="genre_name_case_insensitive_unique",
                violation_error_message = "Genre already exists (case insensitive match)",
            )
        ]

class Language(models.Model):
    """ Model reprensating book language"""

    name = models.CharField(
        max_length=200,
        unique=True,
        null=False,
        help_text="Enter the book natural language(eg. English, French etc)"
    )
    def __str__(self):
        """ String reperensatation of the model object """
        return self.name
    
    def get_absolute_url(self):
        """ returns a URL to access a particular genre"""
        return reverse("language_details", args=[str(self.id)])
    
    class Meta:
        """ Constraints for  unique fields"""
        constraints = [
            UniqueConstraint(
                Lower("name"),
                name="language_name_case_insensitive_unique",
                violation_error_message = "language already exists (case insensitive match)",
            )
        ]


class Author(models.Model):
    """ Model rep. an author"""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField("Died", null=True, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def get_absolute_url(self):
        """ Returns url to access a particular author instance"""
        return reverse("author_detail", args=[str(self.id)])
    
    def __str__(self):
        """ Return a string reprensation of the author object"""

        return f"{self.first_name} {self.last_name}"
    

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.RESTRICT, null=True)
    summary = models.TextField(
        max_length=1000,
        help_text="Entere a brief description of the book"
    )
    isbn = models.CharField("ISBN", max_length=13,
                            unique=True,
                            help_text="13 Character <a href='https://www.isbn-international.org/content/what-isbn'>ISBN number</a>"
                            )

    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book", related_name="genre")
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """ String representation of book object """
        return self.title
    
    def get_absolute_url(self):
        """ Returns the url to access a detail record for a book"""
        return reverse("book_detail", args=[str(self.id)])

    def display_genre(self):
        """ create a sting for the genre. this is requires to to create genre in admin """

        return ",".join(genre.name for genre in self.genre.all())
    display_genre.short_description = "Genre"
    


class BookInstance(models.Model):
    """ Model representing a specific copy of a book(ie. that can be borrowed from a library)"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, 
                          help_text="Unique id for this particular book across the whole library")
    

    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ("m", "Maintenance"),
        ("o", "On loan"),
        ("a", "Available"),
        ("r", "Reserved"),
    )
    status = models.CharField(
        max_length=10,
        choices=LOAN_STATUS,
        blank=True,
        default="m",
        help_text="Book availability"
    )
    borrower = models.ForeignKey(CustomUser,  on_delete=models.SET_NULL, blank=True, null=True)
    class Meta:
        ordering = ["due_back"]
        permissions = [
            ("can_mark_returned", "can mark a book as returned"),
        ]

    def __str__(self):
        return f"{self.id}: ({self.book.title})"
    
    @property
    def is_due(self):
        "Checks if a borrowed book is due"
        return (self.due_back and date.today() > self.due_back)

    


