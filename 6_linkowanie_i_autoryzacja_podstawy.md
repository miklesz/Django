# 6 Linkowanie i autoryzacja podstawy
*[Mikołaj Leszczuk](mailto:mikolaj.leszczuk@agh.edu.pl), [Agnieszka Rudnicka](mailto:rudnicka@agh.edu.pl)*

* Start każdych zajęć
* Linki między modelami
* Formularze w Django
* Podstawy autoryzacji

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

## Linki między filmami, reżyserami i recenzjami

Teraz dodamy linki umożliwiające nawigację między widokami:
- Klikając nazwę filmu w recenzji → przejdziemy do jego widoku
- Klikając reżysera → przejdziemy do jego profilu
- Itd.

---

## Widoki klasowe z linkami

W [`movies/views.py`](http://localhost:8888/edit/movies/views.py):

```python
from django.views.generic import ListView

class MovieListViewWithLinks(ListView):
    model = Movie
    template_name = 'movie_list_with_links.html'

class ReviewListViewWithLinks(ListView):
    model = Review
    template_name = 'review_list_with_links.html'
```

---

## Rejestracja URL

W [`goodmovies/urls.py`](http://localhost:8888/edit/goodmovies/urls.py):

```python
from django.urls import path
from movies.views import MovieListViewWithLinks, ReviewListViewWithLinks

urlpatterns = [
    path('filmy-z-linkami/', MovieListViewWithLinks.as_view(), name='movie-list'),
    path('recenzje-z-linkami/', ReviewListViewWithLinks.as_view(), name='review-list'),
]
```

---

## Szablony z linkami

### Szablon `movie_list_with_links.html`

```django
{% extends 'base.html' %}

{% block content %}
<h1>Filmy</h1>
{% for movie in object_list %}
    <div>
        <h2>{{ movie.title }}</h2>
        <p>{{ movie.short_description }}</p>
        {% if movie.director %}
            <p>Reżyseria: <a href="{% url 'director-detail' movie.director.id %}">
                {{ movie.director.last_name }}
            </a></p>
        {% endif %}
    </div>
{% endfor %}
{% endblock %}
```

### Szablon `review_list_with_links.html`

```django
{% extends 'base.html' %}

{% block content %}
<h1>Recenzje</h1>
{% for review in object_list %}
    <div>
        <p>Film: <a href="{% url 'movie-detail' review.movie.id %}">
            {{ review.movie.title }}
        </a></p>
        <p>{{ review.text }}</p>
        <p>Ocena: {{ review.rating }}★</p>
    </div>
{% endfor %}
{% endblock %}
```

---

## Widok szczegółu (DetailView)

Do wyświetlenia szczegółów pojedynczego obiektu używamy `DetailView`:

```python
from django.views.generic import DetailView

class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movie_detail.html'
```

---

## Rejestracja URL dla DetailView

```python
from django.urls import path
from movies.views import MovieDetailView

urlpatterns = [
    path('film/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('rezyser/<int:pk>/', DirectorDetailView.as_view(), name='director-detail'),
]
```

---

## Podstawy autoryzacji

Django posiada wbudowany system użytkowników i uprawnień.

Ścieżka logowania: [`/accounts/login/`](http://127.0.0.1:8000/accounts/login/)

---

## Formularze rejestracji

Dodajemy url do rejestracji w [`goodmovies/urls.py`](http://localhost:8888/edit/goodmovies/urls.py):

```python
from django.contrib.auth.views import LoginView, LogoutView
from movies.views import user_signup

urlpatterns = [
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/signup/', user_signup, name='signup'),
]
```

---

## Szablony autoryzacji

Szablony przechowujemy w katalogu `movies/templates/registration/`:
- `login.html` — formularz logowania
- `logged_out.html` — strona po wylogowaniu
- `signup.html` — formularz rejestracji

---

## Dalsze prace

1. Stwórz szablony szczegółów dla filmów i reżyserów
2. Dodaj linki zwrotne między modelami
3. Przygotuj szablony autoryzacji
4. Przetestuj logowanie i wylogowanie
