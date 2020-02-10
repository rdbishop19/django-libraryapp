import sqlite3
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from libraryapp.models import Book, Library, model_factory
from .. connection import Connection

@login_required
def library_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = create_library
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT
                    li.id,
                    li.title,
                    li.address,
                    b.id book_id,
                    b.title book_title,
                    b.author,
                    b.year_published,
                    b.isbn
                FROM libraryapp_library li
                JOIN libraryapp_book b ON li.id = b.location_id
            """)

            all_libraries = db_cursor.fetchall()

            library_groups = {}

            for (library, book) in all_libraries:
                # create key if not in dict
                if library.id not in library_groups:
                    library_groups[library.id] = library
                # append book to library in dict
                library_groups[library.id].books.append(book)

        template = 'libraries/list.html'
        context = {
            'all_libraries': library_groups.values(),
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
                INSERT INTO libraryapp_library
                (
                    title,
                    address
                )
                VALUES (?, ?)
            """,
            (
                form_data['title'],
                form_data['address']
            ))

        return redirect(reverse('libraryapp:libraries'))

def create_library(cursor, row):
    _row = sqlite3.Row(cursor, row)

    library = Library()
    library.id = _row["id"]
    library.title = _row["title"]
    library.address = _row["address"]
    library.books = []

    book = Book()
    book.id = _row["book_id"]
    book.title = _row["book_title"]
    book.author = _row["author"]
    book.isbn = _row["isbn"]
    book.year_published = _row["year_published"]

    # Return a tuple containing the library and the
    # book built from the data in the current row of
    # the data set
    return (library, book)