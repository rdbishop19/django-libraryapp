#imports
import sqlite3
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from libraryapp.models import Librarian, model_factory
from .. connection import Connection

#sql function
def get_librarian(librarian_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Librarian)

        db_cursor = conn.cursor()
        db_cursor.execute("""
            SELECT 
                u.username, 
                u.first_name, 
                u.last_name, 
                u.email 
            FROM auth_user u
            WHERE u.id = ?
        """, (librarian_id,))

        return db_cursor.fetchone()

#render function
@login_required
def librarian_details(request, librarian_id):
    if request.method == 'GET':
        librarian = get_librarian(librarian_id)
        template = 'librarians/detail.html'
        context = {
            'librarian': librarian
        }

        return render(request, template, context)