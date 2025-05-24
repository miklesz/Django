"""
URL configuration for goodmovies project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from movies import views

from movies.views import MovieListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', views.hello_world),
    path('filmy/', views.list_movies),  # NOWE
    path('about/', MovieListView.as_view()),
]


from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

from movies.views import DirectorListView
urlpatterns += [
    path("rezyserzy/", DirectorListView.as_view()),
]


from movies.views import ReviewListView
urlpatterns += [
    path("recenzje/", ReviewListView.as_view()),
]


from movies.views import MovieDetailView, DirectorDetailView
urlpatterns += [
    path("film/<int:pk>/", MovieDetailView.as_view(), name="movie-detail"),
    path("rezyser/<int:pk>/", DirectorDetailView.as_view(), name="director-detail"),
]


from movies.views import MovieListViewWithLinks, ReviewListViewWithLinks

urlpatterns += [
    path("movielinks/", MovieListViewWithLinks.as_view()),
    path("reviewlinks/", ReviewListViewWithLinks.as_view()),
]