from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime  # NOWE

# Create your views here.
def hello_world(request):
    our_context = {"time": datetime.now()}  # NOWE
    return render(
        request, 
        template_name="hello.html", 
        context=our_context
    )  # NOWE