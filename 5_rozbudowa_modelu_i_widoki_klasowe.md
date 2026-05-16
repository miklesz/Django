# 5 Rozbudowa modelu i widoki klasowe
*[Mikołaj Leszczuk](mailto:mikolaj.leszczuk@agh.edu.pl), [Agnieszka Rudnicka](mailto:rudnicka@agh.edu.pl)*

* Start każdych zajęć
* Model recenzji
* Widoki klasowe
* Praktyczne wdrożenie

---

## Start każdych zajęć

Na początku wracamy do katalogu kursowego z projektem (tam, gdzie jest `manage.py`).

```bash
cd moj_katalog_kursowy
```

---

## Start każdych zajęć

Aktywujemy środowisko wirtualne:

```bash
# macOS/Linux/WSL
source .venv/bin/activate

# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

Po aktywacji używamy już poleceń typu `python manage.py runserver` oraz `python -m pip install Django`.

---

## Recenzje filmów

Do tej pory mamy modele na filmy i reżyserów. Teraz dodajmy trzeci model — recenzje.

Recenzja będzie zawierać:
- Tekst recenzji
- Ocenę (rating)
- Powiązanie z filmem

---

## Model recenzji

W pliku [`movies/models.py`](http://localhost:8888/edit/movies/models.py) dodajmy model recenzji:

```python
class Review(models.Model):
    RATING_CHOICES = [
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    ]
    
    movie = models.ForeignKey(
        to='movies.Movie',
        verbose_name='film',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(verbose_name='tekst recenzji')
    rating = models.IntegerField(
        verbose_name='ocena',
        choices=RATING_CHOICES,
        default=5
    )
    created_at = models.DateTimeField(
        verbose_name='data utworzenia',
        auto_now_add=True
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'recenzja'
        verbose_name_plural = 'recenzje'
    
    def __str__(self):
        return f"Recenzja do '{self.movie.title}' ({self.rating}★)"
```

---

## Migracje modelu recenzji

Tworzymy migrację:

```bash
python3 manage.py makemigrations
```

Aplikujemy migrację:

```bash
python3 manage.py migrate
```

---

## Rejestracja modeli w admin

Rejestrujemy model recenzji w [`movies/admin.py`](http://localhost:8888/edit/movies/admin.py):

```python
from django.contrib import admin
from movies.models import Movie, Director, Review

admin.site.register(Movie)
admin.site.register(Director)
admin.site.register(Review)  # NOWE
```

---

## Widoki klasowe (Class-Based Views)

Do tej pory pisaliśmy widoki jako zwykłe funkcje. Django oferuje również **widoki klasowe**, które działają bardziej „magicznie".

Widok klasowy to klasa, która dziedziczy po `View` lub jednej z jego podklas.

---

## Podstawowy widok klasowy

```python
from django.views import View
from movies.models import Movie

class MovieListView(View):
    def get(self, request):
        movies = Movie.objects.all()
        return render(
            request,
            template_name='movie_list_v2.html',
            context={'object_list': movies}
        )
```

---

## ListView — gotowy widok do wyświetlenia listy

Przy użyciu `ListView` jest jeszcze prościej:

```python
from django.views.generic import ListView
from movies.models import Movie

class MovieListView(ListView):
    model = Movie
    template_name = 'movie_list_v2.html'
```

ListView automatycznie:
- Pobiera wszystkie obiekty z modelu
- Umieszcza je w kontekście pod nazwą `object_list`
- Renderuje szablon

---

## Rejestracja widoków klasowych w URL

W [`goodmovies/urls.py`](http://localhost:8888/edit/goodmovies/urls.py):

```python
from django.urls import path
from movies.views import MovieListView

urlpatterns = [
    path('filmy-v2/', MovieListView.as_view()),
]
```

---

## Szablon dla ListView

Szablon `movie_list_v2.html`:

```django
{% for movie in object_list %}
    <h2>{{ movie.title }}</h2>
    <p>{{ movie.short_description }}</p>
{% endfor %}
```

---

## Dalsze prace

1. Stwórz `DirectorListView` do wyświetlenia listy reżyserów
2. Stwórz `ReviewListView` do wyświetlenia listy recenzji
3. Przebuduj szablony, aby wykorzystywały `base.html`
4. Dodaj obsługę obrazów reżyserów (pole `photo`)
