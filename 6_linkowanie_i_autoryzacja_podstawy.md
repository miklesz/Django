# 6 Linkowanie i widoki szczegółów
*[Mikołaj Leszczuk](mailto:mikolaj.leszczuk@agh.edu.pl), [Agnieszka Rudnicka](mailto:rudnicka@agh.edu.pl)*

* Start i punkt wyjścia
* `DetailView`
* Adresy z `pk`
* Szablony szczegółów filmu i reżysera
* Linki między filmami, reżyserami i recenzjami
* Typowe błędy przy linkowaniu
* Zadania opcjonalne

---

## Start każdych zajęć

Wracamy do katalogu kursowego z projektem, tam gdzie jest `manage.py`.

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

Po aktywacji możemy używać poleceń Django, np. uruchamiania serwera.

---

## Punkt startowy

Po ćwiczeniu 5 mamy:

- model `Review`,
- listy filmów, reżyserów i recenzji przez `ListView`,
- adresy `/filmy-v2/`, `/rezyserzy/`, `/recenzje/`,
- szablony korzystające z `object_list`.

Teraz dodamy strony szczegółów i linki między obiektami.

---

## `DetailView`

`ListView` pokazuje wiele obiektów.

`DetailView` pokazuje jeden obiekt, np. jeden film albo jednego reżysera.

Django znajdzie konkretny obiekt po identyfikatorze z adresu URL.

Na kolejnych slajdach dodamy szczegóły filmu i reżysera.

---

## Widoki szczegółów

Otwieramy `movies/views.py`:

```bash
nano movies/views.py
```

Do importu widoków klasowych dodajemy `DetailView`.

```python
from django.views.generic import DetailView, ListView
```

Nie kończymy jeszcze edycji tego pliku.

Za chwilę w tym samym `movies/views.py` dopiszemy klasy szczegółów.

---

## Widoki szczegółów

W `movies/views.py` dopisujemy:

```python
class MovieDetailView(DetailView):
    model = Movie
    template_name = "movie_detail.html"


class DirectorDetailView(DetailView):
    model = Director
    template_name = "director_detail.html"
```

Na kolejnym slajdzie wyjaśnimy, skąd widok wie, który obiekt pokazać.

---

## Jak `DetailView` wybiera obiekt?

`DetailView` potrzebuje identyfikatora obiektu.

Najczęściej przekazujemy go w adresie jako `pk`, czyli primary key.

Przykładowe adresy:

| Adres |
|---|
| `/film/1/` |
| `/film/2/` |
| `/rezyser/3/` |

Liczba w adresie mówi, który rekord z bazy ma zostać pokazany.

---

## Rejestracja URL dla szczegółów

Otwieramy `goodmovies/urls.py`:

```bash
nano goodmovies/urls.py
```

Do `urlpatterns` dodajemy:

```python
path("film/<int:pk>/", views.MovieDetailView.as_view(), name="movie-detail"),
path("rezyser/<int:pk>/", views.DirectorDetailView.as_view(), name="director-detail"),
```

Na następnym slajdzie wyjaśnimy, co oznacza fragment `<int:pk>`.

---

## Co oznacza `<int:pk>`?

`<int:pk>` to zmienna część adresu URL.

`int` oznacza, że Django oczekuje liczby całkowitej.

`pk` to nazwa parametru przekazana do widoku.

Dla adresu `/film/5/` widok dostanie `pk=5` i spróbuje znaleźć film o takim ID.

---

## Co oznacza `name="movie-detail"`?

W ćwiczeniu 5 widzieliśmy już `name="movie-list-v2"`.

Tutaj działa ten sam mechanizm.

`name` nadaje ścieżce nazwę.

Dzięki temu w szablonie nie wpisujemy adresu ręcznie.

---

## Przykład użycia `name`

Zamiast pisać adres ręcznie, używamy nazwy trasy.

| Ręcznie wpisany adres | Odwołanie przez nazwę |
|---|---|
| `/film/5/` | nazwa: `movie-detail`, argument: `movie.id` |

Jeśli później zmienimy adres, szablony nadal mogą działać.

---

## Szablon szczegółów filmu

Tworzymy plik:

```bash
nano movies/templates/movie_detail.html
```

W `DetailView` pojedynczy obiekt jest dostępny jako `object`.

---

## `movie_detail.html`

```django
{% extends "base.html" %}

{% block content %}
  <h2>{{ object.title }}</h2>

  {% if object.director %}
    <p>
      Reżyser:
      <a href="{% url 'director-detail' object.director.id %}">
        {{ object.director.first_name }} {{ object.director.last_name }}
      </a>
    </p>
  {% endif %}

  {% if object.premiere_date %}
    <p>Premiera: {{ object.premiere_date }}</p>
  {% endif %}

  {% if object.description %}
    <p>{{ object.description }}</p>
  {% endif %}
{% endblock %}
```

Nowe: `object` i tag `url`. Wyjaśnienie za chwilę.

---

## Co nowego w `movie_detail.html`?

`object` to film znaleziony przez `DetailView`.

`object.director` przechodzi od filmu do reżysera.

Tag `url` buduje adres do szczegółów reżysera.

ID reżysera przekazujemy jako argument adresu.

---

## Szablon szczegółów reżysera

Tworzymy plik:

```bash
nano movies/templates/director_detail.html
```

Pokażemy dane reżysera oraz filmy powiązane przez `related_name="movies"`.

---

## `director_detail.html`

```django
{% extends "base.html" %}

{% block content %}
  <h2>{{ object.first_name }} {{ object.last_name }}</h2>

  {% if object.photo %}
    <img src="{{ object.photo.url }}" alt="{{ object }}">
  {% endif %}

  {% if object.about %}
    <p>{{ object.about }}</p>
  {% endif %}

  <h3>Filmy tego reżysera</h3>
  <ul>
    {% for movie in object.movies.all %}
      <li><a href="{% url 'movie-detail' movie.id %}">{{ movie.title }}</a></li>
    {% empty %}
      <li>Brak filmów tego reżysera.</li>
    {% endfor %}
  </ul>
{% endblock %}
```

Nowe: `object.photo.url` oraz `object.movies.all`. Wyjaśnienie za chwilę.

---

## Co oznacza `object.photo.url`?

`object` to reżyser znaleziony przez `DetailView`.

`object.photo` to plik zdjęcia z pola `ImageField`.

`object.photo.url` to adres zdjęcia dla przeglądarki.

`alt` dostaje tekstową nazwę reżysera.

---

## Co oznacza `object.movies.all`?

Jesteśmy w szablonie szczegółów reżysera.

Tutaj `object` oznacza aktualnego reżysera.

Każdy film ma pole `director`, czyli wskazuje swojego reżysera.

`related_name="movies"` daje przejście w drugą stronę: od reżysera do jego filmów.

---

## Rozbijamy `object.movies.all`

| Fragment | Znaczenie |
|---|---|
| `object` | aktualny reżyser |
| `movies` | filmy tego reżysera |
| `all` | pobierz wszystkie |

Całość oznacza: wszystkie filmy przypisane do aktualnego reżysera.

---

## Sprawdzenie szczegółów

Uruchamiamy serwer:

```bash
python manage.py runserver
```

Sprawdzamy przykładowe adresy:

[http://127.0.0.1:8000/film/1/](http://127.0.0.1:8000/film/1/)

[http://127.0.0.1:8000/rezyser/1/](http://127.0.0.1:8000/rezyser/1/)

Jeśli obiekt o takim ID nie istnieje, Django pokaże błąd 404.

---

## Linki na liście filmów

Otwieramy `movie_list_v2.html`:

```bash
nano movies/templates/movie_list_v2.html
```

Zmienimy tytuł filmu na link do szczegółów.

---

## Link do filmu

W `movie_list_v2.html` szukamy w pętli po filmach:

```django
<strong>{{ movie.title }}</strong>
```

Zastępujemy ten fragment linkiem:

```django
<a href="{% url 'movie-detail' movie.id %}">
  {{ movie.title }}
</a>
```

Tag `url` buduje adres z nazwy `movie-detail` i ID filmu.

---

## Link do reżysera - kiedy?

Link do reżysera robimy tylko wtedy, gdy `movie.director` istnieje.

---

## Link do reżysera - co zastępujemy

W `movie_list_v2.html` szukamy tego fragmentu:

```django
{% if movie.director %}
  <br>Reżyser: {{ movie.director.first_name }} {{ movie.director.last_name }}
{% endif %}
```

Zastąpimy go wersją z linkiem i obsługą braku reżysera.

---

## Link do reżysera - nowy kod

```django
{% if movie.director %}
  <br>
  Reżyser:
  <a href="{% url 'director-detail' movie.director.id %}">
    {{ movie.director.first_name }} {{ movie.director.last_name }}
  </a>
{% else %}
  <br>Reżyser: brak danych
{% endif %}
```

Na kolejnym slajdzie wyjaśnimy, czemu potrzebny jest warunek `if`.

---

## Uwaga na `NoReverseMatch`

Jeśli film nie ma reżysera, `movie.director` jest puste.

Wtedy taki kod może wywołać błąd:

```django
{% url 'director-detail' movie.director.id %}
```

Django nie umie zbudować adresu bez ID reżysera.

Dlatego link do reżysera otaczamy warunkiem sprawdzającym `movie.director`.

---

## Linki na liście recenzji

Otwieramy `review_list.html`:

```bash
nano movies/templates/review_list.html
```

Zmienimy tytuł filmu na link do szczegółów filmu.

---

## `review_list.html` z linkiem

W `review_list.html` szukamy w pętli po recenzjach:

```django
{{ review.movie.title }}: {{ review.text }}
```

Zastępujemy sam tytuł filmu linkiem:

```django
<a href="{% url 'movie-detail' review.movie.id %}">
  {{ review.movie.title }}
</a>
```

To ten sam mechanizm linkowania, tylko ID bierzemy z filmu powiązanego z recenzją.

---

## Link w recenzji - bez `if`

Tutaj nie potrzebujemy `if`, bo recenzja musi mieć przypisany film.

Pole `movie` w modelu `Review` nie ma `null=True`.

---

## Sprawdzenie linków

Wchodzimy na:

[http://127.0.0.1:8000/filmy-v2/](http://127.0.0.1:8000/filmy-v2/)

[http://127.0.0.1:8000/recenzje/](http://127.0.0.1:8000/recenzje/)

Klikamy linki do filmów i reżyserów.

Jeśli pojawia się `NoReverseMatch`, sprawdzamy warunki przy pustych relacjach.

---

## Zadanie opcjonalne 1

Na stronie szczegółów filmu pokaż recenzje tego filmu.

Podpowiedź: w modelu `Review` użyliśmy `related_name="reviews"`.

---

## Rozwiązanie 1

W `movie_detail.html` można dopisać:

```django
<h3>Recenzje</h3>
<ul>
  {% for review in object.reviews.all %}
    <li>{{ review.text }} (ocena: {{ review.rating }})</li>
  {% empty %}
    <li>Brak recenzji tego filmu.</li>
  {% endfor %}
</ul>
```

`object.reviews.all` pobiera recenzje powiązane z aktualnym filmem.

---

## Zadanie opcjonalne 2

Dodaj link powrotny ze szczegółów filmu do listy filmów.

Adres listy to `/filmy-v2/`.

---

## Rozwiązanie 2

W `movie_detail.html` można dopisać:

```django
<p><a href="{% url 'movie-list-v2' %}">Wróć do listy filmów</a></p>
```

Używamy nazwy `movie-list-v2`, którą nadaliśmy ścieżce w `urls.py`.

---

## Zadanie opcjonalne 3

Dodaj link powrotny ze szczegółów reżysera do listy reżyserów.

Nie wpisuj ręcznie adresu `/rezyserzy/`.

Użyj nazwy ścieżki z `urls.py`.

---

## Rozwiązanie 3

W `director_detail.html` można dopisać:

```django
<p><a href="{% url 'director-list' %}">Wróć do listy reżyserów</a></p>
```

Używamy nazwy `director-list`, którą nadaliśmy ścieżce w `urls.py`.
