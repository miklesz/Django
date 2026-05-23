# 4 Prezentacja danych i relacje modeli
*[Mikołaj Leszczuk](mailto:mikolaj.leszczuk@agh.edu.pl), [Agnieszka Rudnicka](mailto:rudnicka@agh.edu.pl)*

* Start i tryb pracy
* Widok listy filmów
* Relacyjne bazy danych
* Model reżysera i relacja z filmem
* Migracje i panel administracyjny
* Konfiguracja plików media
* Zadania opcjonalne

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

Po aktywacji używamy już poleceń typu `python manage.py runserver`.

---

## Punkt startowy

Po ćwiczeniu 3 mamy:

- model `Movie` z polami `title`, `description`, `premiere_date`,
- kilka filmów dodanych w panelu administratora,
- szablon bazowy `base.html`,
- stronę `/hello/`, która potrafi wyświetlić dane z bazy.

Na tych zajęciach zrobimy osobną listę filmów i dodamy relację filmu z reżyserem.

---

## Widok listy filmów

Otwieramy plik `movies/views.py`:

```bash
nano movies/views.py
```

Dodajemy osobny widok listy filmów. Jeśli import `Movie` już istnieje po ćwiczeniu 3, nie dodajemy go drugi raz.

```python
from django.shortcuts import render

from .models import Movie


def hello_world(request):
    movies = Movie.objects.all()
    return render(request, "hello.html", {"movies": movies})


def list_movies(request):
    movies = Movie.objects.all()
    return render(request, "movie_list.html", {"movies": movies})
```

---

## Dlaczego podobny kod?

Na razie `hello_world` i `list_movies` robią prawie to samo: pobierają filmy z bazy i przekazują je do szablonu.

Różnica jest w roli tych widoków:

- `/hello/` zostaje stroną ćwiczeniową z poprzednich zajęć,
- `/filmy/` będzie właściwą listą filmów, którą od teraz rozwijamy.

---

## Rejestracja adresu `/filmy/`

Otwieramy `goodmovies/urls.py`:

```bash
nano goodmovies/urls.py
```

Do `urlpatterns` dodajemy nową ścieżkę:

```python
from django.contrib import admin
from django.urls import path

from movies import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hello/", views.hello_world),
    path("filmy/", views.list_movies),
]
```

---

## Szablon listy filmów

Tworzymy plik `movies/templates/movie_list.html`:

```bash
nano movies/templates/movie_list.html
```

Na początek możemy sprawdzić, czy dane dochodzą do szablonu:

```django
{{ movies }}
```

Po wejściu na [http://127.0.0.1:8000/filmy/](http://127.0.0.1:8000/filmy/) powinniśmy zobaczyć `QuerySet` z filmami.

---

## Pętla w szablonie

Wracamy do tego samego pliku:

```bash
nano movies/templates/movie_list.html
```

Zastępujemy testowe `{{ movies }}` pełnym szablonem.

```django
{% extends "base.html" %}

{% block content %}
  <h2>Filmy</h2>

  <ul>
    {% for movie in movies %}
      <li>
        <strong>{{ movie.title }}</strong>

        {% if movie.premiere_date %}
          <br>Premiera: {{ movie.premiere_date }}
        {% endif %}

        {% if movie.description %}
          <p>{{ movie.description }}</p>
        {% endif %}
      </li>
    {% empty %}
      <li>Brak filmów w bazie.</li>
    {% endfor %}
  </ul>
{% endblock %}
```

Za chwilę rozłożymy najważniejsze linie tego szablonu.

---

## Co robi ten szablon?

`{% extends "base.html" %}` używa wspólnego układu strony.

`{% block content %}` wskazuje miejsce na treść tej strony.

`{% for movie in movies %}` przechodzi po filmach z widoku.

`{{ movie.title }}` i podobne zapisy pobierają pola filmu.

`{% if ... %}` ukrywa puste informacje, a `{% empty %}` obsługuje pustą listę.

---

## Sprawdzenie listy filmów

Odświeżamy stronę:

[http://127.0.0.1:8000/filmy/](http://127.0.0.1:8000/filmy/)

Powinniśmy zobaczyć czytelną listę filmów zamiast technicznego `QuerySet`.

Jeśli widzimy komunikat o braku filmów, sprawdzamy, czy filmy zostały dodane w panelu admina.

---

## Relacyjne bazy danych

Do tej pory nasza aplikacja miała jeden własny model danych: `Movie`.

Każdy film może mieć reżysera. Moglibyśmy dodać do filmu zwykłe pole tekstowe:

```python
director = models.CharField(max_length=128, blank=True)
```

To działa tylko pozornie dobrze.

---

## Problem ze zwykłym polem tekstowym

Jeśli wpisujemy reżysera jako tekst:

- przy kilku filmach tej samej osoby powtarzamy te same dane,
- łatwo zrobić literówki lub różne zapisy tego samego nazwiska,
- zmiana informacji o reżyserze wymaga poprawienia wielu filmów.

Lepsze rozwiązanie to osobny model `Director` i relacja z modelem `Movie`.

---

## Klucz obcy

W relacyjnej bazie danych możemy połączyć dwie tabele.

W naszym przypadku:

- tabela filmów przechowuje filmy,
- tabela reżyserów przechowuje reżyserów,
- film ma pole wskazujące na konkretny rekord z tabeli reżyserów.

Takie pole nazywa się kluczem obcym, czyli `ForeignKey`.

---

## Model reżysera

Otwieramy `movies/models.py`:

```bash
nano movies/models.py
```

Nad modelem `Movie` dodajemy model `Director`:

```python
class Director(models.Model):
    first_name = models.CharField(verbose_name="imię", max_length=100)
    last_name = models.CharField(verbose_name="nazwisko", max_length=100)
    about = models.TextField(verbose_name="o reżyserze", blank=True)
    photo = models.ImageField(
        verbose_name="zdjęcie",
        upload_to="directors/",
        blank=True,
    )

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = "reżyser"
        verbose_name_plural = "reżyserzy"

    def __str__(self):
        return self.first_name + " " + self.last_name
```

---

## Co nowego w modelu `Director`?

`ImageField` pozwala wskazać plik obrazu.

`upload_to="directors/"` mówi, do którego podkatalogu trafią zdjęcia.

`verbose_name` ustawia czytelne nazwy pól w formularzach i panelu admina.

Pola, np. `first_name`, zapisują dane reżysera.

`class Meta` nie zapisuje danych. Ustawia np. sortowanie i nazwy w panelu admina.

`ordering` określa domyślne sortowanie reżyserów.

---

## Co robi `ImageField`

`ImageField` nie zapisuje obrazu bezpośrednio w bazie danych.

W bazie zapisuje się ścieżka do pliku, a sam plik trafia do katalogu z mediami.

Do obsługi obrazów Django potrzebuje biblioteki Pillow. Jeśli jej nie ma, przy sprawdzaniu projektu zobaczymy błąd `fields.E210`.

---

## Pillow

Instalujemy Pillow:

```bash
python -m pip install Pillow
```

Jeśli prowadzimy projekt z plikiem `requirements.txt`, dopisujemy tam zależność:

```text
Pillow
```

Można też odświeżyć cały plik wymagań:

```bash
python -m pip freeze > requirements.txt
```

Sprawdzamy, czy w pliku pojawiło się `Pillow`:

```bash
cat requirements.txt
```

---

## Relacja filmu z reżyserem

W tym samym pliku `movies/models.py` aktualizujemy model `Movie`.

Zostawiamy pola z ćwiczenia 3: `title`, `description`, `premiere_date`.

Dodajemy etykiety oraz pole `director`:

```python
class Movie(models.Model):
    title = models.CharField(verbose_name="tytuł", max_length=200)
    description = models.TextField(verbose_name="opis", blank=True)
    premiere_date = models.DateField(
        verbose_name="data premiery",
        null=True,
        blank=True,
    )
    director = models.ForeignKey(
        to="movies.Director",
        verbose_name="reżyser",
        related_name="movies",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["title"]
        verbose_name = "film"
        verbose_name_plural = "filmy"

    def __str__(self):
        return self.title
```

---

## Dlaczego `null=True` i `blank=True`

Mamy już filmy dodane w bazie po ćwiczeniu 3.

Nie mają jeszcze przypisanych reżyserów, więc nowe pole `director` musi na razie dopuszczać pustą wartość.

- `null=True` pozwala zapisać pustą wartość w bazie danych.
- `blank=True` pozwala zostawić pole puste w formularzu panelu administratora.

Dzięki temu migracja nie zatrzyma się pytaniem o wartość domyślną.

---

## Pełny plik modeli

Po zmianach `movies/models.py` powinien wyglądać podobnie do tego:

```python
from django.db import models


class Director(models.Model):
    first_name = models.CharField(verbose_name="imię", max_length=100)
    last_name = models.CharField(verbose_name="nazwisko", max_length=100)
    about = models.TextField(verbose_name="o reżyserze", blank=True)
    photo = models.ImageField(
        verbose_name="zdjęcie",
        upload_to="directors/",
        blank=True,
    )

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = "reżyser"
        verbose_name_plural = "reżyserzy"

    def __str__(self):
        return self.first_name + " " + self.last_name


class Movie(models.Model):
    title = models.CharField(verbose_name="tytuł", max_length=200)
    description = models.TextField(verbose_name="opis", blank=True)
    premiere_date = models.DateField(
        verbose_name="data premiery",
        null=True,
        blank=True,
    )
    director = models.ForeignKey(
        to="movies.Director",
        verbose_name="reżyser",
        related_name="movies",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["title"]
        verbose_name = "film"
        verbose_name_plural = "filmy"

    def __str__(self):
        return self.title
```

---

## Tworzymy migrację

Najpierw możemy podejrzeć plan migracji:

```bash
python manage.py makemigrations --dry-run --verbosity 3
```

Jeśli nie ma błędu, generujemy migrację:

```bash
python manage.py makemigrations
```

---

## Aplikujemy migrację

Aktualizujemy bazę danych:

```bash
python manage.py migrate
```

Po tym kroku w bazie istnieje tabela reżyserów, a tabela filmów ma nowe pole z relacją do reżysera.

---

## Konfiguracja plików media

Na końcu `goodmovies/settings.py` dodajemy:

```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

To mówi Django, pod jakim adresem i w jakim katalogu obsługiwać pliki wgrywane przez użytkowników.

---

## Udostępnianie media w trybie deweloperskim

W `goodmovies/urls.py` dopisujemy importy:

```python
from django.conf import settings
from django.conf.urls.static import static
```

Na końcu pliku dodajemy:

```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

To rozwiązanie jest przeznaczone do pracy lokalnej przy `DEBUG = True`.

---

## Rejestracja reżyserów w adminie

Otwieramy `movies/admin.py`:

```bash
nano movies/admin.py
```

Rejestrujemy oba modele:

```python
from django.contrib import admin

from .models import Director, Movie

admin.site.register(Director)
admin.site.register(Movie)
```

Jeśli `Movie` był już zarejestrowany po ćwiczeniu 3, dodajemy tylko import `Director` i linię `admin.site.register(Director)`.

---

## Kontrola w panelu admin

Uruchamiamy serwer:

```bash
python manage.py runserver
```

Wchodzimy do panelu:

[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

Powinna pojawić się sekcja reżyserów. Dodajemy 1-2 reżyserów, a potem edytujemy istniejące filmy i przypisujemy im reżysera.

---

## Reżyser na liście filmów

Możemy teraz uzupełnić `movie_list.html` o reżysera:

```django
{% if movie.director %}
  <br>Reżyser: {{ movie.director.first_name }} {{ movie.director.last_name }}
{% endif %}
```

Ten fragment wkładamy wewnątrz pętli `{% for movie in movies %}`.

---

## Zadania opcjonalne

1. W szablonie `movie_list.html` wyświetl osobno tytuł, opis, datę premiery i reżysera każdego filmu.
2. Popraw wygląd listy prostym HTML-em i CSS-em.
3. Dodaj widok szczegółów pierwszego filmu pod adresem `/pierwszy-film/`.
4. W panelu admin dodaj zdjęcie reżysera i sprawdź, czy plik pojawia się w katalogu `media/`.

---

## Rozwiązania

Zadanie 1, przykład wnętrza pętli:

```django
<li>
  <strong>{{ movie.title }}</strong>
  {% if movie.premiere_date %}
    <br>Premiera: {{ movie.premiere_date }}
  {% endif %}
  {% if movie.director %}
    <br>Reżyser: {{ movie.director.first_name }} {{ movie.director.last_name }}
  {% endif %}
  {% if movie.description %}
    <p>{{ movie.description }}</p>
  {% endif %}
</li>
```

Zadanie 2, prosty CSS w `base.html`:

```html
<style>
  body { font-family: Arial, sans-serif; max-width: 800px; margin: 2rem auto; }
  li { margin-bottom: 1rem; }
</style>
```

---

## Rozwiązania

Zadanie 3, widok w `movies/views.py`:

```python
def first_movie(request):
    movie = Movie.objects.first()
    return render(request, "first_movie.html", {"movie": movie})
```

Adres w `goodmovies/urls.py`:

```python
path("pierwszy-film/", views.first_movie),
```

Szablon `movies/templates/first_movie.html`:

```django
{% extends "base.html" %}

{% block content %}
  {% if movie %}
    <h2>{{ movie.title }}</h2>
    <p>{{ movie.description }}</p>
  {% else %}
    <p>Brak filmów w bazie.</p>
  {% endif %}
{% endblock %}
```

Zadanie 4: po zapisaniu zdjęcia w adminie plik powinien trafić do `media/directors/`.
