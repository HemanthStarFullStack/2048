from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required

def home_page(request):
    
    return render(request, 'page.html')