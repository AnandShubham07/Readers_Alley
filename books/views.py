from django.shortcuts import render,redirect
from .models import Book,IssuedBook,LibraryUser
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from datetime import date, timedelta
from django.db import connection, transaction
from django.utils import timezone
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Max


def home(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        title = request.POST.get('title')
        author = request.POST.get('author')

        Book.objects.create(
            book_id=book_id,
            title=title,
            author=author,
            available=True
        )

        return redirect('home')

    books = Book.objects.all()
    return render(request, 'books/home.html', {'books': books})
def browse_books(request):
    books = Book.objects.all()
    return render(request, 'books/browse_books.html', {'books': books})



def login_view(request):
    role = request.POST.get('role',request.GET.get('role','user'))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            if role == 'admin' and not user.is_staff:
                return render(request, 'books/login.html', {
                    'role': role,
                    'error': 'You do not have admin access.'
                })

            if role != 'admin' and user.is_staff:
                return render(request, 'books/login.html', {
                    'role': role,
                    'error': 'Please use the admin login.'
                })

            login(request, user)

            if user.is_staff:
                return redirect('admin_dashboard')

            return redirect('user_dashboard')

        return render(request, 'books/login.html', {
            'role': role,
            'error': 'Invalid username or password.'
        })

    return render(request, 'books/login.html', {'role': role})


def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def user_dashboard(request):
    if request.user.is_staff:
        return HttpResponseForbidden("Access denied.")

    return render(request, 'books/user_dashboard.html')


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Access denied.")

    return render(request, 'books/admin_dashboard.html')

@login_required
def add_book(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Access denied.")

    error = None
    success = None

    if request.method == 'POST':
        book_id = request.POST.get('book_id', '').strip()
        title = request.POST.get('title', '').strip()
        author = request.POST.get('author', '').strip()

        if not book_id or not title or not author:
            error = "All fields are required."

        elif Book.objects.filter(book_id=book_id).exists():
            error = "A book with this ID already exists."

        else:
            Book.objects.create(
                book_id=book_id,
                title=title,
                author=author,
                available=True
            )
            success = "Book added successfully!"

    return render(request, 'books/add_book.html', {
        'error': error,
        'success': success
    })
@login_required
def issue_book(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Access denied.")

    message = ""
    users = LibraryUser.objects.all().order_by('user_id')
    if request.method == "POST":
        book_id = request.POST.get("book_id", "").strip()
        user_id = request.POST.get("user_id", "").strip()
        if not LibraryUser.objects.filter(user_id=user_id).exists():
            message = "Please select a valid registered user."
        try:
            with transaction.atomic():
                book = Book.objects.select_for_update().get(
                    book_id=book_id
                )

                if book.available is False:
                    message = "This book is already issued."
                else:
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            SELECT 1 FROM issued_books
                            WHERE book_id = %s AND return_date IS NULL
                        """, [book_id])

                        if cursor.fetchone():
                            message = "This book is already issued."
                        else:
                            today = timezone.localdate()

                            cursor.execute("""
                                INSERT INTO issued_books
                                (user_id, book_id, issue_date, due_date, return_date)
                                VALUES (%s, %s, %s, %s, NULL)
                            """, [
                                user_id,
                                book_id,
                                today,
                                today + timedelta(days=14)
                            ])

                            book.available = False
                            book.save(update_fields=["available"])
                            message = "Book issued successfully!"

        except Book.DoesNotExist:
            message = "Book ID not found."
        except Exception:
            message = "Unable to issue book. Check the book and user IDs."

    books = Book.objects.filter(available=True)

    return render(request, "books/issue_book.html", {
        "books": books,
        "users":users,
        "message": message
    })


@login_required
def return_book(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Access denied.")

    message = ""

    if request.method == "POST":
        book_id = request.POST.get("book_id", "").strip()

        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT issue_id FROM issued_books
                        WHERE book_id = %s AND return_date IS NULL
                        ORDER BY issue_id DESC
                        LIMIT 1
                        FOR UPDATE
                    """, [book_id])

                    issue = cursor.fetchone()

                    if not issue:
                        message = "No active issue found for this book."
                    else:
                        cursor.execute("""
                            UPDATE issued_books
                            SET return_date = %s
                            WHERE issue_id = %s
                        """, [timezone.localdate(), issue[0]])

                        Book.objects.filter(book_id=book_id).update(
                            available=True
                        )
                        message = "Book returned successfully!"

        except Exception:
            message = "Unable to return book. Check the book ID."

    return render(request, "books/return_book.html", {
        "message": message
    })

def get_next_user_id():
    user_ids = LibraryUser.objects.values_list('user_id', flat=True)

    numeric_ids = [
        int(uid) for uid in user_ids
        if uid.isdigit()
    ]

    return str(max(numeric_ids) + 1) if numeric_ids else "101"

@login_required
def add_user(request):
    if not request.user.is_staff:
        return redirect('home')

    if request.method == 'POST':
        user_id = request.POST.get('user_id', '').strip()
        name = request.POST.get('name', '').strip()

        if not user_id or not name:
            messages.error(request, "All fields are required.")

        elif len(user_id) > 20:
            messages.error(request, "User ID cannot exceed 20 characters.")

        elif len(name) > 100:
            messages.error(request, "Name cannot exceed 100 characters.")

        elif LibraryUser.objects.filter(user_id=user_id).exists():
            messages.error(request, "This User ID is already registered.")

        else:
            try:
                with transaction.atomic():
                    LibraryUser.objects.create(
                        user_id=user_id,
                        name=name
                    )
                messages.success(request, "User registered successfully!")
                return redirect('user_list')

            except IntegrityError:
                messages.error(request, "This User ID is already registered.")


    next_user_id=get_next_user_id()
    return render(request, 'books/add_user.html',{'next_user_id':next_user_id})


@login_required
def user_list(request):
    if not request.user.is_staff:
        return redirect('home')

    users = LibraryUser.objects.all().order_by('user_id')

    return render(request, 'books/user_list.html', {
        'users': users
    })


@login_required
def issue_history(request):
    if not request.user.is_staff:
        return redirect('home')

    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()

    query = """
        SELECT
            ib.issue_id,
            ib.user_id,
            u.name,
            ib.book_id,
            b.title,
            ib.issue_date,
            ib.due_date,
            ib.return_date,

            CASE
                WHEN ib.return_date IS NOT NULL THEN 'Returned'
                WHEN ib.due_date < CURRENT_DATE THEN 'Overdue'
                ELSE 'Issued'
            END AS status,

            GREATEST(
                COALESCE(ib.return_date, CURRENT_DATE) - ib.due_date,
                0
            ) AS overdue_days,

            GREATEST(
                COALESCE(ib.return_date, CURRENT_DATE) - ib.due_date,
                0
            ) * 5 AS fine

        FROM issued_books ib
        JOIN users u ON ib.user_id = u.user_id
        JOIN books b ON ib.book_id = b.book_id
        WHERE 1=1
    """

    params = []

    if search:
        query += """
            AND (
                ib.user_id ILIKE %s OR
                u.name ILIKE %s OR
                ib.book_id ILIKE %s OR
                b.title ILIKE %s
            )
        """
        search_value = f"%{search}%"
        params.extend([search_value] * 4)

    if status == 'Issued':
        query += " AND ib.return_date IS NULL AND ib.due_date >= CURRENT_DATE"

    elif status == 'Overdue':
        query += " AND ib.return_date IS NULL AND ib.due_date < CURRENT_DATE"

    elif status == 'Returned':
        query += " AND ib.return_date IS NOT NULL"

    query += " ORDER BY ib.issue_date DESC, ib.issue_id DESC"

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        columns = [column[0] for column in cursor.description]
        records = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    return render(request, 'books/issue_history.html', {
        'records': records,
        'search': search,
        'selected_status': status,
    })




