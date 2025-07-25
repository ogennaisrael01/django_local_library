from django.core.management.base import BaseCommand
from catalog.models import Genre, Language, Author, Book, BookInstance
from faker import Faker
import random
from datetime import timedelta, date

fake = Faker()

class Command(BaseCommand):
    help = "Seed the library database with sample data"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Seeding data..."))

        # Clear existing data (optional, be careful!)
        # Genre.objects.all().delete()
        # Language.objects.all().delete()
        # Author.objects.all().delete()
        # Book.objects.all().delete()
        # BookInstance.objects.all().delete()

        # Seed Genres
        genres = ['Fantasy', 'Romance', 'Horror', 'Mystery', "Science FIction"]
        genre_objs = [Genre.objects.create(name=g) for g in genres]

        # Seed Languages
        languages = ['English', 'French', 'German', 'Spanish']
        language_objs = [Language.objects.create(name=l) for l in languages]

        # Seed Authors
        author_objs = []
        for _ in range(10):
            author = Author.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                date_of_birth=fake.date_of_birth(minimum_age=30, maximum_age=80),
                date_of_death=None if random.random() > 0.3 else fake.date_this_century(before_today=True)
            )
            author_objs.append(author)

        # Seed Books
        book_objs = []
        for _ in range(15):
            book = Book.objects.create(
                title=fake.sentence(nb_words=4),
                author=random.choice(author_objs),
                summary=fake.paragraph(nb_sentences=3),
                isbn=fake.isbn13(separator=""),
                language=random.choice(language_objs)
            )
            # Assign random genres
            book.genre.set(random.sample(genre_objs, k=random.randint(1, 3)))
            book_objs.append(book)

        # Seed Book Instances
        for _ in range(25):
            BookInstance.objects.create(
                book=random.choice(book_objs),
                imprint=fake.company(),
                due_back=fake.date_between(start_date="+1d", end_date="+30d"),
                status=random.choice(['m', 'o', 'a', 'r'])
            )

        self.stdout.write(self.style.SUCCESS("Seeding complete! 🎉"))
