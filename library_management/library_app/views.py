from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied

from .models import Category, Author, Book, Member, BorrowerList
from .forms import (LoginForm, BookForm, CategoryForm, MemberForm, 
                    BorrowerForm, AuthorForm, BookSearchForm)

# Authentication Login
def loginView(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            theme = form.cleaned_data.get('theme', 'light')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                request.session['theme'] = theme
                print('------------', theme, request.session['theme'])
                messages.success(request, "Login Successfull")
                return redirect('dashboard')
            else:
                messages.error(request, "Error Occured")
    return render(request, 'loginPage.html', {'form': form})

# Authentication Logout
def logoutView(request):
    logout(request)
    messages.success(request, "Logged out Successfully")
    return redirect("login")

# Dashboard view
@login_required(login_url='login')
def dashboardView(request):
    total_books = Book.objects.all().count()
    total_members = Member.objects.all().count()
    total_books_borrowed = BorrowerList.objects.filter(returned=False).count()
    over_due = BorrowerList.objects.filter(due_date__lt=timezone.now().date(), returned=False)

    return render(request, 'dashboard.html', {'user': request.user,
                                             'total_books': total_books,
                                             'total_members': total_members,
                                             'total_books_borrowed': total_books_borrowed,
                                             'over_due': over_due,
                                             'over_due_count': over_due.count(),})

# Category CRUD Operations
@login_required(login_url='login')
def create_category(request):
    form = CategoryForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Category Created Successfully")
            return redirect('listCategory')
        else:
            messages.error(request, "Error Occured")
    return render(request, "createUpdateForm.html", {'form': form,
                                                     'title': 'Create Category',
                                                     'return_book': False,})
def pagination(request, querySet, page_size):
    paginator = Paginator(querySet, page_size)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

@login_required(login_url='login')
def list_category(request):
    category = Category.objects.all()
    page_obj = pagination(request, category, 10)
    return render(request, 'listForm.html', {'page_obj': page_obj,
                                             'title': 'Book Categories',
                                             'dynamic_update_url': 'updateCategory',
                                             'dynamic_delete_url': 'deleteCategory',
                                             'model': 'category',})

@login_required(login_url='login')
def update_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Updated Successfully")
            return redirect('listCategory')
        else:
            messages.error(request, "Error Occured")
    return render(request, 'createUpdateForm.html', {'form': form,
                                                     'title': 'Update Category',
                                                     'return_book': False,})

@login_required(login_url='login')
def delete_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    category.delete()
    messages.success(request, "Deleted Successfully")
    return redirect("listCategory")

# Authors CRUD Operations
@login_required(login_url='login')
def create_author(request):
    form = AuthorForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Author Created Successfully")
            return redirect('listAuthor')
        else:
            messages.error(request, "Error Occured")
    return render(request, "createUpdateForm.html", {'form': form,
                                                     'title': 'Create Author',
                                                     'return_book': False,})

@login_required(login_url='login')
def list_author(request):
    authors = Author.objects.all()
    page_obj = pagination(request, authors, 10)
    return render(request, 'listForm.html', {'page_obj': page_obj,
                                             'title': 'Book Authors',
                                             'dynamic_update_url': 'updateAuthor',
                                             'dynamic_delete_url': 'deleteAuthor',
                                             'model': 'author',})

@login_required(login_url='login')
def update_author(request, pk):
    author = get_object_or_404(Author, id=pk)
    form = AuthorForm(request.POST or None, instance=author)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Updated Successfully")
            return redirect('listAuthor')
        else:
            messages.error(request, "Error Occured")
    return render(request, 'createUpdateForm.html', {'form': form,
                                                     'title': 'Update Author',
                                                     'return_book': False,})

@login_required(login_url='login')
def delete_author(request, pk):
    author = get_object_or_404(Author, id=pk)
    author.delete()
    messages.success(request, "Deleted Successfully")
    return redirect("listAuthor")

# Members CRUD Operations
@login_required(login_url='login')
def create_member(request):
    form = MemberForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Member Created Successfully")
            return redirect('listMember')
        else:
            messages.error(request, "Error Occured")
    return render(request, "createUpdateForm.html", {'form': form, 
                                                     'title': 'Create Member',
                                                     'return_book': False,})

@login_required(login_url='login')
def list_member(request):
    members = Member.objects.all()
    page_obj = pagination(request, members, 10)
    return render(request, 'listForm.html', {'page_obj': page_obj,
                                             'title': 'Library Members',
                                             'dynamic_update_url': 'updateMember',
                                             'dynamic_delete_url': 'deleteMember',
                                             'model': 'member',})

@login_required(login_url='login')
def update_member(request, pk):
    member = get_object_or_404(Member, id=pk)
    form = MemberForm(request.POST or None, instance=member)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Updated Successfully")
            return redirect('listMember')
        else:
            messages.error(request, "Error Occured")
    return render(request, 'createUpdateForm.html', {'form': form,
                                                     'title': 'Update Member',
                                                     'return_book': False,})

@login_required(login_url='login')
def delete_member(request, pk):
    member = get_object_or_404(Member, id=pk)
    member.delete()
    messages.success(request, "Deleted Successfully")
    return redirect("listMember")

# Book CRUD Operations
@login_required(login_url='login')
def create_book(request):
    form = BookForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Book Created Successfully")
            return redirect('listBook')
        else:
            messages.error(request, "Error Occured")
            print(form.errors)
    return render(request, "createUpdateForm.html", {'form': form,
                                                     'title': 'Create Book',
                                                     'return_book': False,})

@login_required(login_url='login')
def list_book(request):
    form = BookSearchForm(request.GET or None)
    books = Book.objects.all()

    if form.is_valid():
        q = form.cleaned_data['query']
        if q:
            books = books.filter(
                title__icontains=q
            ) | books.filter(
                author__name__icontains=q
            ) | books.filter(
                category__name__icontains=q
            )

    page_obj = pagination(request, books, 10)
    return render(request, 'listForm.html', {'page_obj': page_obj,
                                             'title': 'Library Books',
                                             'dynamic_update_url': 'updateBook',
                                             'dynamic_delete_url': 'deleteBook',
                                             'model': 'book',
                                             'form': form})

@login_required(login_url='login')
def update_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    form = BookForm(request.POST or None, instance=book)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Updated Successfully")
            return redirect('listBook')
        else:
            messages.error(request, "Error Occured")
    return render(request, 'createUpdateForm.html', {'form': form,
                                                     'title': 'Update Book',
                                                     'return_book': False,})

@login_required(login_url='login')
def delete_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    book.delete()
    messages.success(request, "Deleted Successfully")
    return redirect("listBook")

# Checking the user is a librarian
def is_librarian(user):
    if user.is_authenticated and user.groups.filter(name='Librarian').exists():
        return True
    elif not user.is_authenticated:
        return False  # triggers redirect to login
    else:
        raise PermissionDenied

# Borrower CRUD Operations
@user_passes_test(is_librarian, login_url='/login/')
def borrow_book(request):
    form = BorrowerForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid(): 
            borrow_rec = form.save(commit=False)           # Unsaved instance 
            book = borrow_rec.book

            if book.stock <= 0:
                messages.error(request, "Error Occured")
            else: 
                borrow_rec.save()
                book.stock -= 1
                book.save()
                messages.success(request, "Borrower entry Created Successfully")
                return redirect('listBorrower')
        else:
            messages.error(request, "Error Occured")
    return render(request, "createUpdateForm.html", {'form': form,
                                                     'title': 'Borrow Book',
                                                     'return_book': False,})

@login_required(login_url='login')
def list_borrower(request):
    borrowers_list = BorrowerList.objects.all()
    page_obj = pagination(request, borrowers_list, 10)
    return render(request, 'listForm.html', {'page_obj': page_obj,
                                                 'title': 'Borrowers List',
                                                 'model': 'borrower',})

@user_passes_test(is_librarian, login_url='/login/')
def return_book(request, pk):
    borrower = get_object_or_404(BorrowerList, id=pk)
    form = BorrowerForm(request.POST or None, instance=borrower)

    if request.method == 'POST':
        if form.is_valid():
            borrow_obj = form.save(commit=False)
            borrow_obj.returned = True
            borrow_obj.return_date = timezone.now().date()
            borrow_obj.save()

            book = borrow_obj.book
            book.stock += 1
            bk = book.save()
            messages.success(request, "Updated Successfully")
            return redirect('listBorrower')
        else:
            messages.error(request, "Error Occured")
    return render(request, 'createUpdateForm.html', {'form': form,
                                               'borrower': borrower,
                                               'title': 'Return Book',
                                               'return_book': True})
# Book listing search

def book_list(request):
    form = BookSearchForm(request.GET or None)
    books = Book.objects.all()

    if form.is_valid():
        q = form.cleaned_data['query']

        if q:
            books = books.filter(
                title__icontains=q
            ) | books.filter(
                author__icontains=q
            ) | books.filter(
                category__icontains=q
            )

    return render(request, 'book_list.html', {
        'form': form,
        'books': books
    })