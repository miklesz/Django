from django.contrib import admin

from movies.models import Movie, Director, Review

# Register your models here.
admin.site.register(Movie)  # NOWE
admin.site.register(Director) # nowe
admin.site.register(Review)
