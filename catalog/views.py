from django.shortcuts import render, redirect
from .models import Book, BookInstance, Author, Language, Genre, CustomUser
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm
# Create your views here.
@login_required
def index(request):
    """ view function for the home page"""
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # available books (status = "a")
    num_instances_available = BookInstance.objects.filter(status="a").count()
    num_authors = Author.objects.all().count()
    genre = Genre.objects.all().count()

    num_of_visits = request.session.get("num_of_visits", 0)
    num_of_visits += 1
    request.session["num_of_visits"] = num_of_visits

    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
         "genre": genre,
         "num_of_visits": num_of_visits
    }

    return render(request, "index.html", context=context)

class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    
@login_required
def detailview(request, id):
    book = get_object_or_404(Book, id=id)
    context = {"book": book}

    return render(request,"catalog/book_detail.html", context)
@login_required
def list_authors(request):
    try: 
        authors = Author.objects.all()
        context = {
            "authors":authors
        }
    except Author.DoesNotExist as e:
        return Http404(f"Error: {e}")
    return render(request, "catalog/author_list.html", context)

class AuthorDetialView(LoginRequiredMixin, generic.DetailView):
    model = Author
    template_name = "catalog/author_details.html"
    context_object_name = "author"

    def get_queryset(self):
        return super().get_queryset().filter(pk=self.kwargs["pk"])


def registerview(request):
    try:
        if request.method == "POST":
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("login")
        else:
            form = UserRegisterForm()
        return render(request, "catalog/register.html", context={"form": form})
    
    except Exception as e:
        return f"Error {e}"

@login_required        
def loaned_book_view(request):
    try:
        borrowed_books = BookInstance.objects.filter(borrower=request.user).filter(status="o").order_by("-due_back")
        if borrowed_books is None:
            return None
        
        context = {
            "borrowed_books": borrowed_books
        }
        return render(request, "catalog/borrowed_book.html", context)
    except BookInstance.DoesNotExist:
        return None


@login_required
@permission_required("catalog.can_mark_returned", raise_exception=True)
def staff_Loaned_book_view(request):

    try:
        borrowed_books = BookInstance.objects.filter(status__iexact="o")
        if borrowed_books is None:
            return None
        context = {
            "borrowed_books": borrowed_books
        }
        return render(request, "catalog/liberians_borrowed_books.html", context)
    except Exception or BookInstance.DoesNotExist:
        return None
    