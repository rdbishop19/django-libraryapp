import sqlite3
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required
from libraryapp.models import Book
from libraryapp.models import model_factory
from .. connection import Connection

def get_book(book_id):
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
            WHERE b.id = ?
        """, (book_id,))

        return db_cursor.fetchone()

@login_required
def book_details(request, book_id):
    if request.method == 'GET':
        book = get_book(book_id)

        template = 'books/detail.html'
        context = {
            'book': book
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        # EDIT BOOK
        if (
            "actual_method" in form_data and form_data['actual_method'] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                    UPDATE libraryapp_book
                    SET title = ?,
                        author = ?,
                        isbn = ?,
                        year_published = ?,
                        location_id = ?
                    WHERE id = ?
                """,
                (
                    form_data['title'],
                    form_data['author'],
                    form_data['isbn'],
                    form_data['year_published'],
                    form_data['location'],
                    book_id,
                ))

            return redirect(reverse('libraryapp:books'))
            
        # check if this POST is for deleting a book
        # parentheses to break up complex `if` statements for readability
        if (
            "actual_method" in form_data and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                    DELETE FROM libraryapp_book
                    WHERE id = ?
                """, (book_id,))

            return redirect(reverse('libraryapp:books'))