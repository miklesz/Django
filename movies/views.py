from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime  

from movies.models import Movie  # NOWE


# Create your views here.


def hello_world(request):
    our_context = {"time": datetime.now()}
    return render(
        request, 
        template_name="hello.html", 
        context=our_context
    )


def list_movies(request):
    movies = Movie.objects.all()
    return render(
        request, 
        template_name="movie_list.html", 
        context={"movies": movies}
    )  # NOWE