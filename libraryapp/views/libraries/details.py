#imports
import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from libraryapp.models import Library, model_factory
from .. connection import Connection

def get_library(library_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Library)

        db_cursor = conn.cursor()
        db_cursor.execute("""
            SELECT
                l.id,
                l.title,
                l.address
            FROM libraryapp_library l
            WHERE l.id = ?
        """, (library_id,))

        return db_cursor.fetchone()

@login_required
def library_details(request, library_id):
    if request.method == 'GET':
        library = get_library(library_id)
        template = 'libraries/detail.html'
        context = {
            'library': library
        }

        return render(request, template, context)

#define render function