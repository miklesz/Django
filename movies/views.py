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


from django.views.generic import ListView
from .models import Movie
class MovieListView(ListView):
    model = Movie
    template_name = "movie_list_v2.html"

    
from .models import Director
class DirectorListView(ListView):
    model = Director
    template_name = "director_list.html"
    
    
from .models import Review
class ReviewListView(ListView):
    model = Review
    template_name = "review_list.html"
    
    
from django.views.generic import DetailView
class MovieDetailView(DetailView):
    model = Movie
    template_name = "movie_detail.html"
class DirectorDetailView(DetailView):
    model = Director
    template_name = "director_detail.html"
    
    
class MovieListViewWithLinks(ListView):
    model = Movie
    template_name = "movie_list_with_links.html"
class ReviewListViewWithLinks(ListView):
    model = Review
    template_name = "review_list_with_links.html"
