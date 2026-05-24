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

Dodajemy osobny widok listy filmów.

Jeśli import `Movie` już istnieje, nie dodajemy go drugi raz.

```python
from .models import Movie


def list_movies(request):
    movies = Movie.objects.all()
    return render(request, "movie_list.html", {"movies": movies})
```

Na kolejnym slajdzie wyjaśnimy, czemu ten widok przypomina `hello_world`.

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

Jeśli serwer nie działa, uruchamiamy go:

```bash
python manage.py runserver
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

`{% if ... %}` ukrywa puste informacje.

`{% empty %}` wykona się, gdy `for` nie ma żadnego filmu do pokazania.

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

Na kolejnym slajdzie pokażemy tę relację jako prosty diagram.

---

## Diagram relacji

Tak możemy myśleć o modelach po dzisiejszej zmianie:

```text
Director 1 ─── wiele Movie
```

Jeden reżyser może mieć wiele filmów.

Jeden film wskazuje jednego reżysera albo na razie nie ma go przypisanego.

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

Na kolejnych slajdach wyjaśnimy nowe elementy tego modelu.

---

## Co nowego w modelu `Director`?

`ImageField` pozwala wskazać plik obrazu; za chwilę wyjaśnimy to dokładniej.

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

Edytujemy istniejący model `Movie`:

```bash
nano movies/models.py
```

Dopisujemy pole `director` wewnątrz obecnej klasy.

```python
    director = models.ForeignKey(
        to="movies.Director",
        verbose_name="reżyser",
        related_name="movies",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
```

Na kolejnym slajdzie zobaczymy, jak wygląda cała klasa `Movie` po tej zmianie.

---

## Co tu się zmienia?

Pola `title`, `description` i `premiere_date` są z ćwiczenia 3.

Przy tych polach dopisujemy teraz `verbose_name`, czyli polskie etykiety dla formularzy.

Nowe pole to `director`.

Nowe ustawienia klasy to `Meta`: sortowanie i nazwy modelu w panelu admina.

---

## Model `Movie` po zmianie

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

Na kolejnych slajdach wyjaśnimy nowe elementy pola `director`.

---

## Co nowego przy `director`?

`ForeignKey` łączy film z jednym reżyserem.

`to="movies.Director"` wskazuje model, do którego prowadzi relacja.

`related_name="movies"` pozwala później przejść od reżysera do jego filmów.

`on_delete=models.CASCADE` oznacza: jeśli usuniemy reżysera, Django usunie też jego filmy.

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

Otwieramy `goodmovies/settings.py`:

```bash
nano goodmovies/settings.py
```

Na końcu pliku dodajemy:

```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

To mówi Django, pod jakim adresem i w jakim katalogu obsługiwać pliki wgrywane przez użytkowników.

---

## Udostępnianie media w trybie deweloperskim

Otwieramy `goodmovies/urls.py`:

```bash
nano goodmovies/urls.py
```

Zrobimy w nim dwie edycje: importy na górze i dopisek pod `urlpatterns`.

Na górze pliku dopisujemy:

```python
from django.conf import settings
from django.conf.urls.static import static
```

---

## Udostępnianie media w trybie deweloperskim

Pod `urlpatterns` w tym samym pliku dodajemy:

```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Na kolejnym slajdzie wyjaśnimy, po co ten fragment jest potrzebny.

---

## Po co dopisujemy media do `urls.py`?

`MEDIA_ROOT` mówi, gdzie Django zapisuje wgrane pliki.

Ale przeglądarka potrzebuje jeszcze adresu URL, pod którym może je pobrać.

Ten wpis sprawia, że lokalnie adresy typu `/media/directors/plik.jpg` będą działać.

W prawdziwym wdrożeniu pliki media zwykle serwuje serwer WWW, nie Django.

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

Otwieramy szablon listy filmów:

```bash
nano movies/templates/movie_list.html
```

Nie usuwamy daty premiery, opisu ani `{% empty %}`.

Dopisujemy tylko fragment z reżyserem, np. pod tytułem filmu:

```django
{% if movie.director %}
  <br>Reżyser: {{ movie.director.first_name }} {{ movie.director.last_name }}
{% endif %}
```

---

## `movie_list.html` po zmianie

```django
{% extends "base.html" %}

{% block content %}
  <h2>Filmy</h2>

  <ul>
    {% for movie in movies %}
      <li>
        <strong>{{ movie.title }}</strong>

        {% if movie.director %}
          <br>Reżyser: {{ movie.director.first_name }} {{ movie.director.last_name }}
        {% endif %}

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

---

## Sprawdzenie listy z reżyserem

Odświeżamy stronę:

[http://127.0.0.1:8000/filmy/](http://127.0.0.1:8000/filmy/)

Przy filmach z przypisanym reżyserem powinniśmy zobaczyć jego imię i nazwisko.

Jeśli reżyser się nie pojawia, sprawdzamy w panelu admina, czy film ma przypisanego reżysera.

---

## Zadanie opcjonalne 1

W `movie_list.html` pokaż informację także wtedy, gdy film nie ma przypisanego reżysera.

Zamiast pomijać reżysera, wyświetl:

```text
Reżyser: brak danych
```

---

## Rozwiązanie 1

Edytujemy tylko warunek `if movie.director`.

W `movies/templates/movie_list.html` może wyglądać tak:

```django
{% if movie.director %}
  <br>Reżyser: {{ movie.director.first_name }} {{ movie.director.last_name }}
{% else %}
  <br>Reżyser: brak danych
{% endif %}
```

`{% else %}` działa wtedy, gdy warunek z `if` nie jest spełniony.

---

## Zadanie opcjonalne 2

Popraw wygląd listy filmów prostym CSS-em.

Wystarczy zmienić wspólny szablon `base.html`, żeby styl zadziałał na wszystkich stronach.

---

## Rozwiązanie 2

Otwieramy `base.html`:

```bash
nano movies/templates/base.html
```

W sekcji `<head>` dodajemy:

```html
<style>
  body { font-family: Arial, sans-serif; max-width: 800px; margin: 2rem auto; }
  li { margin-bottom: 1rem; }
</style>
```

---

## Zadanie opcjonalne 3

Dodaj w `movies/views.py` widok `first_movie`.

Widok ma pobrać pierwszy film z bazy i przekazać go do szablonu `first_movie.html`.

---

## Rozwiązanie 3

Otwieramy `movies/views.py`:

```bash
nano movies/views.py
```

Dopisujemy:

```python
def first_movie(request):
    movie = Movie.objects.first()
    return render(request, "first_movie.html", {"movie": movie})
```

`Movie.objects.first()` zwraca pierwszy film albo `None`, jeśli baza jest pusta.

---

## Zadanie opcjonalne 4

Podłącz widok z poprzedniego zadania pod adresem:

[http://127.0.0.1:8000/pierwszy-film/](http://127.0.0.1:8000/pierwszy-film/)

---

## Rozwiązanie 4

Otwieramy `goodmovies/urls.py`:

```bash
nano goodmovies/urls.py
```

Do `urlpatterns` dopisujemy:

```python
path("pierwszy-film/", views.first_movie),
```

---

## Zadanie opcjonalne 5

Utwórz szablon `first_movie.html`.

Ma pokazać tytuł i opis filmu albo informację, że w bazie nie ma filmów.

---

## Rozwiązanie 5

Tworzymy szablon:

```bash
nano movies/templates/first_movie.html
```

Dopisujemy:

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

---

## Zadanie opcjonalne 6

W panelu admin dodaj zdjęcie reżysera.

Potem sprawdź, czy plik pojawił się w katalogu `media/directors/`.

---

## Rozwiązanie 6

W panelu admin otwieramy reżysera, wybieramy plik w polu `zdjęcie` i zapisujemy formularz.

W terminalu sprawdzamy katalog:

```bash
ls media/directors
```

Jeśli plik jest widoczny, upload działa.
