# 4 Prezentacja danych i relacje modeli
*[Mikołaj Leszczuk](mailto:mikolaj.leszczuk@agh.edu.pl), [Agnieszka Rudnicka](mailto:rudnicka@agh.edu.pl)*

* Prezentacja danych
* Relacyjne bazy danych
* Ulepszamy modele

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

## Widok listy filmów

Udajmy się do [`movies/views.py`](http://localhost:8888/edit/movies/views.py) aby utworzyć widok listy filmów.

Na dobry początek trzeba zaimportować model (mądre IDE jak PyCharm lub VSCode same to zaproponują/zrobią).
Następnie piszemy kolejną funkcję, która przyjmuje zapytanie (`request`) jako argument.

```python
from movies.models import Movie  # NOWE

def list_movies(request):
    movies = Movie.objects.all()
    return render(
        request, 
        template_name="movie_list.html", 
        context={"movies": movies}
    )  # NOWE
```

W tym miejscu wiele się dzieje! Zacznijmy od góry:

* dzięki zaimportowaniu modelu `Movie` będziemy mogli wejść w interakcje z bazą danych za pośrednictwem Django, czyli między innymi:
  * dodawać nowe obiekty typu `Movie`
  * edytować i usuwać istniejące obiekty `Movie`
  * odczytywać a także filtrować istniejące obiekty `Movie`

* `objects` - każdy model w Django ma coś co się nazywa [manager](https://docs.djangoproject.com/en/stable/topics/db/managers/), nie będziemy wchodzić tutaj w szczegóły, ale jest to interfejs przez który dostarczane są nam operacje na bazie danych. W praktyce, umożliwia to nam tworzenie, edycję, usuwanie i inne zapytania do bazy danych.

* `Movie.objects.all()` użyje menedżera obiektów typu `Movie` i zapyta bazę danych o WSZYSTKIE filmy. Dostaniemy więc listę całej zawartości naszej filmoteki.

* Do wygenerowania odpowiedzi aplikacji zostanie użyty szablon `movie_list.html` (tak, musimy go teraz stworzyć!)

* Lista filmów zostanie dodana do kontekstu HTML

---

## Rejestracja podstrony listy filmów

Aby widok mógł być wyświetlony trzeba mu przydzielić jakiś adres. Udajmy się więc do [`urls.py`](http://localhost:8888/edit/goodmovies/urls.py) czyli o URL resolvera naszego projektu. Tutaj należy dodać `path()`, który będzie kierował zapytania przeglądarek użytkowników z konkretnego adresu na stronę powstającej listy filmów.

Przykładowo, do listy `urlpatterns` dodajmy linijkę:

```python
urlpatterns = [
    ...
    
    # http://127.0.0.1:8000/filmy/
    path('filmy/', views.list_movies),  # NOWE
]
```

Teraz link [http://127.0.0.1:8000/filmy/](http://127.0.0.1:8000/filmy/) powinien nas kierować do listy filmów, którą przed chwilą napisaliśmy w [`views.py`](http://localhost:8888/edit/movies/views.py). Został jeszcze jeden element - szablon HTML, który wyświetli dane.

---

## Szablon HTML listy

Stwórzmy plik o nazwie [`movie_list.html`](http://localhost:8888/edit/movies/templates/movie_list.html) (oczywiście musi być umieszczony w katalogu szablonów naszej aplikacji [`movies/templates/`](movies/templates/)).


```python
!touch movies/templates/movie_list.html
```

Na początek możemy sprawdzić, czy wszystko dobrze zaprogramowaliśmy. Spróbujmy więc wypisać zmienną `movies`, którą dodaliśmy do kontekstu szablonu.

```django
{{ movies }}
```

Jeśli w przeglądarce pojawiła się lista obiektów z tajemniczym `QuerySet`, to jesteśmy na dobrej drodze.

Aby wypisać elementy list prostą pętlą można posłużyć się tagiem Django

`{% for %}`.

```django
{% for movie in movies %}
<p>
    Film: "{{ movie }}"
</p>
{% endfor %}
```

Powyższy kawałek kodu prze-iteruje po liście, którą dostarczyliśmy z widoku. Następnie dla każdego elementu wstawi HTML zawarty w środku, czyli w naszym przypadku akapit z napisem `Film: "{{ movie }}"`.

---

## Dalsze prace

1. Wypisz osobno każde z pól modelu filmu np.: tytuł (`movie.title`), datę publikacji (`movie.published_at`)
2. Wykorzystaj HTML (np.: `<b></b>`, `<i></i>`) i CSS (np.: `<style>p {color: green;}</style>`) do poprawienia wyglądu listy
3. Przebuduj szablon `movie_list.html` tak aby wykorzystywał (rozszerzał) szablon bazowy `base.html` (np.: `{% extends "base.html" %}{% block content %}{% endblock %}`)
4. Dodaj widok szczegółów pierwszego, pojedynczego filmu (np.: `Movie.objects.all()[0]`)

---

## Relacyjne bazy danych

Do tej pory nasza aplikacja posiadała dość prosty i ubogi model danych. Była to tylko pojedyncza tabela przechowująca filmy (`class Movie(models.Model)` w pliku [`movies/models.py`](http://localhost:8888/edit/movies/models.py)).

Pora na utworzenie oddzielnego modelu na reżyserów i recenzje oraz rozszerzenie istniejącego modelu filmów o dodatkowe pola.

---

## Problem z polem reżysera w obecnym modelu

Wróćmy do pliku z naszymi modelami, [`movies/models.py`](http://localhost:8888/edit/movies/models.py). Gdybyśmy umieścili pole na reżysera:

```python
class Movie(models.Model):
    ...
    director = models.CharField(null=True, max_length=128)
```

To napotkamy następujące problemy:

- Jeśli mamy kilka filmów tego samego reżysera, to informacje o nim się powtarzają w wielu wpisach (redundancja danych)
- Jest większa szansa popełnienia błędu i powstania różnych zapisów tego samego imienia/nazwiska
- Przy aktualizacji informacji o reżyserze trzeba zaktualizować wszystkie filmy

---

## Relacje i klucz obcy

Jedną z podstawowych zalet baz danych, które używamy (SQLite, PostgreSQL i innych), jest możliwość tworzenia relacji między modelami.

Rozwiązaniem jest wydzielenie osobnej tabeli na dane o reżyserach. W ten sposób będziemy mieli:
- Filmy w jednej tabeli
- Reżyserów w drugiej

Bazy relacyjne pozwalają zdefiniować specjalne pole (klucz obcy), w którym będzie przechowywany identyfikator wiersza z innej tabeli.

Każdy model w Django ma automatycznie pole `id` — **klucz główny**, który jednoznacznie identyfikuje jeden wiersz.

---

## Graficzna reprezentacja modelu danych

Aby było łatwiej zrozumieć co z czym się łączy, tworzy się modele danych np. przy pomocy UML (Unified Modeling Language).

Poniższy diagram UML przedstawia aplikację [źródło: MDN]:

![](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django/Models/local_library_model_uml.svg)

---

## Ulepszamy nasze modele

Stwórzmy osobny model na reżysera i wykorzystajmy mechanizmy baz relacyjnych do stworzenia powiązań z filmami.

---

## Model reżysera

W pliku [`movies/models.py`](http://localhost:8888/edit/movies/models.py) dodajmy model reżysera:

```python
class Director(models.Model):
    first_name = models.CharField(verbose_name="imię", max_length=100)
    last_name = models.CharField(verbose_name="nazwisko", max_length=100)
    about = models.TextField(verbose_name="o reżyserze", blank=True)
    photo = models.ImageField(verbose_name="zdjęcie", blank=True)
    
    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = "reżyser"
        verbose_name_plural = "reżyserzy"
        
    def __str__(self):
        return self.first_name + " " + self.last_name
```

---

## Pole ImageField

Model zawiera pole na imię, nazwisko, opis oraz zdjęcie (obraz graficzny).

Django pozwala nam tworzyć pola, które przechowują ścieżkę do pliku. Rzadko kiedy przechowuje się pliki wgrane przez użytkowników w bazie danych — Django domyślnie w polu `ImageField` przechowuje tylko informacje o nazwie pliku.

---

## Etykieta `verbose_name`

`verbose_name` to domyślna etykieta wyświetlana w panelu administratora.

Dzięki temu zabiegowi, zamiast angielskich nazw zmiennych zobaczymy polskie etykiety.

---

## Meta-dane modelu (`class Meta`)

Tutaj definiuje się meta-dane dotyczące modelu:
- `ordering`: domyślne sortowanie elementów
- `verbose_name`, `verbose_name_plural`: nazwy wyświetlane w panelu admin

Sortowanie po nazwisku/imieniu jest dla nas (ludzi) naturalne i jest szczególnie ważne przy widokach z paginacją.

---

## Poprawki w modelu filmów

Skoro już wzbogacamy nasz model o etykiety, dodajmy je również do modelu filmu:

```python
class Movie(models.Model):
    title = models.CharField(verbose_name="tytuł", max_length=100)
    short_description = models.TextField(verbose_name="opis")
    published_at = models.DateField(verbose_name="data premiery")

    # Klucz obcy do reżysera
    director = models.ForeignKey(
        to="movies.Director",
        verbose_name="reżyser",
        related_name="movies",
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        ordering = ["title"]
        verbose_name = "film"
        verbose_name_plural = "filmy"

    def __str__(self):
        return self.title
```

Pole `director` to teraz klucz obcy (`ForeignKey`), który łączy film z reżyserem.
