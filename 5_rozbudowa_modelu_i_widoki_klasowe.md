# 5 Rozbudowa modelu i widoki klasowe
*[Mikołaj Leszczuk](mailto:mikolaj.leszczuk@agh.edu.pl), [Agnieszka Rudnicka](mailto:rudnicka@agh.edu.pl)*

* Start i punkt wyjścia
* Model recenzji
* Migracje i panel administracyjny
* Widoki klasowe `ListView`
* Listy filmów, reżyserów i recenzji
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

Po aktywacji używamy poleceń typu `python manage.py runserver`.

---

## Punkt startowy

Po ćwiczeniu 4 mamy:

- model `Movie`,
- model `Director`,
- relację filmu z reżyserem,
- listę filmów pod `/filmy/`,
- obsługę plików media dla zdjęć reżyserów.

Teraz dodamy recenzje i pokażemy listy danych przez widoki klasowe.

---

## Recenzje filmów

Recenzja będzie osobnym modelem powiązanym z filmem.

Chcemy przechowywać:

- film, którego dotyczy recenzja,
- tekst recenzji,
- ocenę,
- datę dodania.

---

## Model recenzji

Otwieramy `movies/models.py`:

```bash
nano movies/models.py
```

Pod modelem `Movie` dodajemy model `Review`.

---

## Model recenzji

```python
class Review(models.Model):
    RATING_CHOICES = [
        (1, "★"),
        (2, "★★"),
        (3, "★★★"),
        (4, "★★★★"),
        (5, "★★★★★"),
    ]

    movie = models.ForeignKey(
        to="movies.Movie",
        verbose_name="film",
        related_name="reviews",
        on_delete=models.CASCADE,
    )
    text = models.TextField(verbose_name="tekst recenzji")
    rating = models.IntegerField(
        verbose_name="ocena",
        choices=RATING_CHOICES,
        default=5,
    )
    created_at = models.DateTimeField(
        verbose_name="data utworzenia",
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "recenzja"
        verbose_name_plural = "recenzje"

    def __str__(self):
        return f"Recenzja do: {self.movie.title}"
```

Na kolejnym slajdzie wyjaśnimy nowe elementy modelu.

---

## Co nowego w `Review`?

`choices=RATING_CHOICES` ogranicza ocenę do kilku wartości.

`auto_now_add=True` automatycznie zapisuje datę utworzenia recenzji.

`related_name="reviews"` pozwoli później przejść od filmu do jego recenzji.

`ordering = ["-created_at"]` sortuje od najnowszych recenzji.

---

## Migracje modelu recenzji

Tworzymy migrację:

```bash
python manage.py makemigrations
```

Aplikujemy migrację:

```bash
python manage.py migrate
```

---

## Podgląd migracji

Dla kontroli możemy sprawdzić katalog migracji:

```bash
ls movies/migrations
```

Najnowszy plik migracji powinien dodawać model `Review`.

Jeśli chcemy go podejrzeć, otwieramy plik z najwyższym numerem, np.:

```bash
cat movies/migrations/0003_review.py
```

---

## Rejestracja recenzji w adminie

Otwieramy `movies/admin.py`:

```bash
nano movies/admin.py
```

Jeśli `Movie` i `Director` są już zarejestrowane, dodajemy tylko `Review`.

```python
from .models import Director, Movie, Review

admin.site.register(Review)
```

---

## Kontrola w panelu admin

Uruchamiamy serwer:

```bash
python manage.py runserver
```

Wchodzimy do panelu:

[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

Powinna pojawić się sekcja recenzji. Dodajemy 2-3 recenzje do istniejących filmów.

---

## Widoki funkcyjne i klasowe

Do tej pory pisaliśmy widoki jako funkcje, np. `list_movies`.

Widok funkcyjny sam pobiera dane i sam wywołuje `render`.

Widok klasowy pozwala użyć gotowej klasy Django, która robi część pracy za nas.

Najpierw użyjemy `ListView`, czyli gotowego widoku listy obiektów.

---

## Najprostszy widok klasowy

Widok klasowy może reagować osobno na różne metody HTTP.

```python
from django.http import HttpResponse
from django.views import View


class MyView(View):
    def get(self, request):
        return HttpResponse("GET")

    def post(self, request):
        return HttpResponse("POST")
```

My za chwilę użyjemy gotowej klasy `ListView`, więc nie będziemy pisać `get` ręcznie.

---

## `ListView`

`ListView` automatycznie:

- pobiera obiekty z podanego modelu,
- przekazuje je do szablonu jako `object_list`,
- renderuje wskazany szablon.

My musimy podać przede wszystkim `model` i `template_name`.

---

## Widok klasowy listy filmów

Otwieramy `movies/views.py`:

```bash
nano movies/views.py
```

Dodajemy import `ListView` i klasy widoków.

---

## Widok klasowy listy filmów

```python
from django.views.generic import ListView

from .models import Director, Movie, Review


class MovieListView(ListView):
    model = Movie
    template_name = "movie_list_v2.html"
```

Na kolejnym slajdzie wyjaśnimy, co Django zrobi za nas.

---

## Co robi `MovieListView`?

`model = Movie` mówi, że widok pracuje na filmach.

`template_name = "movie_list_v2.html"` mówi, którego szablonu użyć.

Nie piszemy tutaj `Movie.objects.all()`.

`ListView` zrobi to automatycznie i przekaże wynik jako `object_list`.

---

## Rejestracja widoku w URL

Otwieramy `goodmovies/urls.py`:

```bash
nano goodmovies/urls.py
```

Do `urlpatterns` dodajemy:

```python
path("filmy-v2/", views.MovieListView.as_view(), name="movie-list-v2"),
```

`as_view()` zamienia klasę widoku na widok, który Django może wywołać dla żądania HTTP.

---

## Szablon dla `ListView`

Tworzymy szablon:

```bash
nano movies/templates/movie_list_v2.html
```

W widoku klasowym lista obiektów jest dostępna jako `object_list`.

---

## `movie_list_v2.html`

```django
{% extends "base.html" %}

{% block content %}
  <h2>Filmy z widoku klasowego</h2>

  <ul>
    {% for movie in object_list %}
      <li>
        <strong>{{ movie.title }}</strong>
        {% if movie.director %}
          <br>Reżyser: {{ movie.director.first_name }} {{ movie.director.last_name }}
        {% endif %}
      </li>
    {% empty %}
      <li>Brak filmów w bazie.</li>
    {% endfor %}
  </ul>
{% endblock %}
```

---

## Sprawdzenie `/filmy-v2/`

Odświeżamy albo uruchamiamy serwer:

```bash
python manage.py runserver
```

Wchodzimy na:

[http://127.0.0.1:8000/filmy-v2/](http://127.0.0.1:8000/filmy-v2/)

Powinniśmy zobaczyć listę filmów z nowego widoku klasowego.

---

## Lista reżyserów i recenzji

Ten sam mechanizm możemy zastosować do innych modeli.

W `movies/views.py` dopisujemy:

```python
class DirectorListView(ListView):
    model = Director
    template_name = "director_list.html"


class ReviewListView(ListView):
    model = Review
    template_name = "review_list.html"
```

---

## URL dla list

W `goodmovies/urls.py` dopisujemy:

```python
path("rezyserzy/", views.DirectorListView.as_view(), name="director-list"),
path("recenzje/", views.ReviewListView.as_view(), name="review-list"),
```

Po tym potrzebujemy jeszcze dwóch szablonów.

---

## Szablon listy reżyserów

Tworzymy plik:

```bash
nano movies/templates/director_list.html
```

```django
{% extends "base.html" %}

{% block content %}
  <h2>Reżyserzy</h2>

  <ul>
    {% for director in object_list %}
      <li>{{ director.first_name }} {{ director.last_name }}</li>
    {% empty %}
      <li>Brak reżyserów w bazie.</li>
    {% endfor %}
  </ul>
{% endblock %}
```

---

## Szablon listy recenzji

Tworzymy plik:

```bash
nano movies/templates/review_list.html
```

```django
{% extends "base.html" %}

{% block content %}
  <h2>Recenzje</h2>

  <ul>
    {% for review in object_list %}
      <li>
        {{ review.movie.title }}: {{ review.text }}
        <br>Ocena: {{ review.rating }}
      </li>
    {% empty %}
      <li>Brak recenzji w bazie.</li>
    {% endfor %}
  </ul>
{% endblock %}
```

---

## Co oznacza `review.movie.title`?

`review` to jedna recenzja z pętli.

`review.movie` to film powiązany z tą recenzją przez `ForeignKey`.

`review.movie.title` to tytuł tego filmu.

Django pozwala tak przechodzić po relacjach w szablonach.

---

## Sprawdzenie list

Sprawdzamy w przeglądarce:

[http://127.0.0.1:8000/rezyserzy/](http://127.0.0.1:8000/rezyserzy/)

[http://127.0.0.1:8000/recenzje/](http://127.0.0.1:8000/recenzje/)

Jeśli lista recenzji jest pusta, wracamy do panelu admina i dodajemy recenzje.

---

## Zadanie opcjonalne 1

W `review_list.html` dodaj datę utworzenia recenzji.

Podpowiedź: pole nazywa się `created_at`.

---

## Rozwiązanie 1

Wewnątrz pętli w `review_list.html` można dopisać:

```django
<br>Dodano: {{ review.created_at }}
```

Cały fragment recenzji może wtedy pokazywać film, tekst, ocenę i datę.

---

## Zadanie opcjonalne 2

W `director_list.html` pokaż opis reżysera, ale tylko wtedy, gdy pole `about` nie jest puste.

---

## Rozwiązanie 2

Wewnątrz pętli po reżyserach można użyć:

```django
{% if director.about %}
  <p>{{ director.about }}</p>
{% endif %}
```

Warunek chroni przed pustym akapitem przy reżyserach bez opisu.
