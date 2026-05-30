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

## Model recenzji - pola

To jest pierwsza część tej samej klasy `Review`.

Dzielimy edycję na dwa slajdy tylko po to, żeby osobno omówić pola i ustawienia modelu.

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
```

Na następnym slajdzie dopiszemy ustawienia tej samej klasy.

---

## Model recenzji - ustawienia

To nadal jest ta sama klasa `Review`.

Nie tworzymy drugiej klasy. Ten fragment wklejamy dalej wewnątrz `Review`, pod polami z poprzedniego slajdu.

```python
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "recenzja"
        verbose_name_plural = "recenzje"

    def __str__(self):
        return f"Recenzja do: {self.movie.title}"
```

Na kolejnym slajdzie wyjaśnimy nowe elementy modelu.

---

## Co nowego w `Review`? - pola

`choices=RATING_CHOICES` ogranicza ocenę do kilku wartości.

W bazie zapisze się liczba, np. `5`.

`auto_now_add=True` automatycznie zapisuje datę utworzenia recenzji.

`related_name="reviews"` pozwoli później przejść od filmu do jego recenzji.

---

## Co nowego w `Review`? - ustawienia

`ordering = ["-created_at"]` ustawia domyślną kolejność recenzji.

Minus przed `created_at` oznacza sortowanie malejące, czyli najnowsze recenzje jako pierwsze.

`get_rating_display()` omówimy później przy szablonie recenzji.

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

Dla kontroli możemy sprawdzić, czy migracja aplikacji `movies` jest wykonana:

```bash
python manage.py showmigrations movies
```

---

## Rejestracja recenzji w adminie

Otwieramy `movies/admin.py`:

```bash
nano movies/admin.py
```

Jeśli `Movie` i `Director` są już zarejestrowane, zostawiamy ich linie.

Dopisujemy `Review` do importu i dodajemy rejestrację `Review`.

Finalnie fragment może wyglądać tak:

```python
from .models import Director, Movie, Review

admin.site.register(Director)
admin.site.register(Movie)
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

Powinna pojawić się sekcja recenzji.

Dodajemy 2-3 recenzje do istniejących filmów.

---

## Widoki funkcyjne i klasowe

Do tej pory pisaliśmy widoki jako funkcje, np. `list_movies`.

Widok funkcyjny sam pobiera dane i sam wywołuje `render`.

Widok klasowy pozwala użyć gotowej klasy Django, która robi część pracy za nas.

Najpierw użyjemy `ListView`, czyli gotowego widoku listy obiektów.

---

## Mapa widoków klasowych

To jest ogólna idea, nie fragment do wpisywania w projekcie.

```text
View
`-- ListView
    |-- MovieListView
    |-- DirectorListView
    `-- ReviewListView
```

`View` to ogólny mechanizm widoku klasowego.

`ListView` to gotowy widok do list obiektów.

Nasze klasy dopasują `ListView` do konkretnych modeli.

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

---

## Widok klasowy listy filmów

Dodajemy import `ListView` i klasę widoku.

Jeśli import modeli już istnieje, dopisujemy `Director` i `Review` do tej samej linii.

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

## Co robi `name=`?

`name="movie-list-v2"` pojawia się tu po raz pierwszy.

`"filmy-v2/"` to adres wpisywany w przeglądarce.

`name="movie-list-v2"` to nazwa tego adresu wewnątrz Django.

Później w szablonie będzie można napisać:

```django
{% url 'movie-list-v2' %}
```

i Django samo zbuduje adres `/filmy-v2/`.

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

## Co robi `movie_list_v2.html`?

`extends` i `block` działają tak samo jak we wcześniejszych szablonach.

Nowością jest `object_list`, czyli lista przekazana automatycznie przez `ListView`.

`{% for movie in object_list %}` przechodzi po filmach.

`movie.director.first_name` to znany już mechanizm przechodzenia po relacji z filmu do reżysera.

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

Otwieramy `movies/views.py`:

```bash
nano movies/views.py
```

Dopisujemy:

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

Otwieramy `goodmovies/urls.py`:

```bash
nano goodmovies/urls.py
```

Do istniejącego `urlpatterns` dopisujemy:

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

## Co robi `director_list.html`?

Mechanizm jest taki sam jak przy filmach.

`object_list` zawiera teraz reżyserów, bo `DirectorListView` ma `model = Director`.

`director` to pojedynczy reżyser z pętli.

Pokazujemy jego zwykłe pola: `first_name` i `last_name`.

---

## Szablon listy recenzji

Tworzymy plik:

```bash
nano movies/templates/review_list.html
```

W szablonie pojawi się zapis `review.movie.title`.

To ten sam typ przejścia po relacji, który widzieliśmy wcześniej przy `movie.director.first_name`.

Tutaj przechodzimy od recenzji do filmu.

```django
{% extends "base.html" %}

{% block content %}
  <h2>Recenzje</h2>

  <ul>
    {% for review in object_list %}
      <li>
        {{ review.movie.title }}: {{ review.text }}
        <br>Ocena: {{ review.get_rating_display }}
      </li>
    {% empty %}
      <li>Brak recenzji w bazie.</li>
    {% endfor %}
  </ul>
{% endblock %}
```

---

## Relacja: `review.movie.title`

`review` to jedna recenzja z pętli.

`review.movie` to film powiązany z tą recenzją przez `ForeignKey`.

`review.movie.title` to tytuł tego filmu.

Django pozwala tak przechodzić po relacjach w szablonach.

---

## Ocena z gwiazdkami

`rating` jest polem z `choices=RATING_CHOICES`.

W bazie zapisuje się liczba, np. `5`.

W szablonie chcemy pokazać etykietę, czyli gwiazdki:

```django
{{ review.get_rating_display }}
```

---

## Skąd ta nazwa?

Django tworzy metodę według wzoru:

```text
get_<nazwa_pola>_display
```

Dla pola `rating` powstaje `get_rating_display`.

W szablonie Django zapisujemy metodę bez nawiasów.

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

## Przygotowanie do zadania 2

Do następnego zadania potrzebujemy reżysera z pustym polem `about`.

Jeśli już taki jest w bazie, nic nie zmieniamy.

Jeśli każdy reżyser ma opis, w panelu admina dodajemy albo edytujemy jednego reżysera i zostawiamy `about` puste.

---

## Zadanie opcjonalne 2

W `director_list.html` pokaż opis reżysera z etykietą:

```text
Opis:
```

Cały fragment `Opis: ...` ma pojawić się dopiero wtedy, gdy pole `about` nie jest puste.

---

## Rozwiązanie 2

Wewnątrz pętli po reżyserach można użyć:

```django
{% if director.about %}
  <p>Opis: {{ director.about }}</p>
{% endif %}
```

Warunek chroni przed pustym akapitem `Opis:` przy reżyserach bez opisu.

---

## Zadanie opcjonalne 3

W widoku klasowym `MovieListView` posortuj filmy alfabetycznie po tytule.

Podpowiedź: `ListView` może mieć ustawienie `ordering`.

---

## Rozwiązanie 3

W `movies/views.py` dopisujemy jedną linię w klasie `MovieListView`:

```python
class MovieListView(ListView):
    model = Movie
    template_name = "movie_list_v2.html"
    ordering = ["title"]
```

To zmienia kolejność filmów tylko w widoku `/filmy-v2/`.

---

## Zadanie opcjonalne 4

W `movie_list_v2.html` pokaż przy każdym filmie liczbę jego recenzji.

Podpowiedź: w modelu `Review` użyliśmy `related_name="reviews"`.

---

## Rozwiązanie 4

Wewnątrz pętli po filmach można dopisać:

```django
<br>Recenzji: {{ movie.reviews.count }}
```

`movie.reviews` przechodzi od filmu do jego recenzji.

`count` liczy, ile takich recenzji jest w bazie.
