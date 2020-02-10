from django.urls import include, path
from .views import *

app_name = "libraryapp"

urlpatterns = [
    #admin
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', logout_user, name='logout'),
    
    #regular user
    path('', home, name='home'),
    path('books/', book_list, name='books'),
    path('books/<int:book_id>', book_details, name='book'),
    path('librarians/', librarian_list, name='librarians'),
    path('librarians/<int:librarian_id>', librarian_details, name='librarian'),
    path('libraries/', library_list, name='libraries'),
    path('libraries/<int:library_id>', library_details, name='library'),
    path('book/form', book_form, name='book_form'),
    path('library/form', library_form, name='library_form'),
]