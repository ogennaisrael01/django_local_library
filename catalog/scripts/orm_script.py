from catalog.models import Author, Book, Genre, Language, CustomUser, BookInstance

# function to run the ORM scripts
    # Create an instance for the author model
    # author1 = Author.objects.create(
    #     first_name="John",
    #     last_name="Doe",
    #     date_of_birth="1909-01-18"
    # # )
    # # author2 = Author.objects.create(
    # #      first_name="Ada",
    # #     last_name="lovelace",
    # #     date_of_birth="1902-01-18"
    # # )

    # # Create an instance for the language model
    # # language1 = Language.objects.get_or_create(name="Hindi")
    # # language2 = Language.objects.get_or_create(name="French")


    # # Inctances for the Book model

    # # book, created = Book.objects.get_or_create(
    # #     title="Puple Hibisscus",
    # #     author= Author.objects.filter(first_name__iexact="Amanda"),
    # #     summary="",
    # #     isbn="6789054321234",
    # #     language=Language.objects.get(name__startswith="E")
    # # )

    # # book.genre.add(Genre.objects.filter(name="Fiction"))
   

    # all_authors = Author.objects.all()
    # all_books = Book.objects.all()

    # print("\nALl authors")
    # for author in all_authors:
    #     print(f"Author: {author.first_name} {author.last_name}, Date of Birth: {author.date_of_birth}")

    # print(f"\nAll books")

    # for book in all_books:
        # print(f"Book: {book.title}, Author: {book.author.first_name} {book.author.last_name}, Language: {book.language.name}")



def run():
    user = CustomUser.objects.get(email="john.smith@example.com")
    if user is None:
        return None
    
    bookinstance = BookInstance.objects.get(book__title__iexact="Stock From")
    if bookinstance is None:
        return None
    bookinstance.borrower = user
    bookinstance.save()
    print("saved")
run()