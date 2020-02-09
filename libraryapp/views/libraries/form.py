from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def library_form(request):
    if request.method == 'GET':
        template = 'libraries/form.html'

        return render(request, template)