import sqlite3
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from libraryapp.models import Book
from libraryapp.models import model_factory
from .. connection import Connection

@login_required
def book_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:

            conn.row_factory = model_factory(Book)

            db_cursor = conn.cursor()
            db_cursor.execute("""
                SELECT
                    b.id,
                    b.title,
                    b.isbn,
                    b.author,
                    b.year_published,
                    b.librarian_id,
                    b.location_id
                FROM libraryapp_book b
            """)

            all_books = db_cursor.fetchall()

        template = 'books/list.html'
        context = {
            'all_books': all_books
        }

        return render(request, template, context)
    
    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute(""" 
                INSERT INTO libraryapp_book
                (
                    title, 
                    author, 
                    isbn,
                    year_published, 
                    location_id, 
                    librarian_id
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                form_data['title'], 
                form_data['author'], 
                form_data['isbn'],
                form_data['year_published'], 
                form_data['location'],
                request.user.librarian.id # request has the user/librarian info available here
            ))

        return redirect(reverse('libraryapp:books'))

