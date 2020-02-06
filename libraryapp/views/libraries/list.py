import sqlite3
from django.shortcuts import render
from libraryapp.models import Library
from .. connection import Connection

def library_list(request):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                l.id,
                l.title,
                l.address
            FROM libraryapp_library l
        """)

        all_libraries = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            lib = Library()
            # assign properties here
            lib.title = row['title']
            lib.address = row['address']

            all_libraries.append(lib)

    template = 'libraries/list.html'
    context = {
        'all_libraries': all_libraries
    }

    return render(request, template, context)