import sqlite3
from django.shortcuts import render
from libraryapp.models import Librarian, model_factory
from .. connection import Connection

def librarian_list(request):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Librarian)
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                l.id,
                l.location_id,
                l.user_id,
                u.first_name,
                u.last_name,
                u.email
            FROM libraryapp_librarian l
            JOIN auth_user u ON l.user_id = u.id
        """)

        all_librarians = db_cursor.fetchall()

    template = 'librarians/list.html'
    context = {
        'all_librarians': all_librarians
    }

    return render(request, template, context)