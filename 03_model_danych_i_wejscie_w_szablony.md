# 03 Model danych i wejście w szablony
*[Mikołaj Leszczuk](mailto:mikolaj.leszczuk@agh.edu.pl), [Agnieszka Rudnicka](mailto:rudnicka@agh.edu.pl)*

* Model danych — po co nam baza danych?
* Klasyczna vs. Django podejście do baz
* Tworzenie migracji i modelu
* Jak włączyć obsługę Django w PyCharm (opcjonalnie)
* Zadanie

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

## Tryb pracy na zajęciach

- Terminal: uruchamianie komend Django
- Terminal + `nano`: domyślny tryb pracy na kursie
- `cat`: szybki podgląd plików bez edycji
- IDE (PyCharm/VS Code): opcjonalnie, szczegóły na końcu lekcji

---

## Po co nam baza danych?

Baza danych to po prostu kontener, w którym zapisane będą informacje o różnych rzeczach — użytkownikach, filmach, recenzjach, itp.

Najprościej mówiąc: zamiast pamiętać wszystko w pamięci programu, zapisujemy dane na dysku w uporządkowany sposób.

---

## Po co nam baza danych?

Na potrzeby kursu będziemy tworzyć mini-bibliotekę zawierającą filmy, czyli modele do przechowywania informacji o filmach, reżyserach, recenzjach.

Zobaczmy, jak to działa w praktyce.

---

## „Klasyczne" zarządzanie bazami danych

Gdybyśmy pracowali bezpośrednio z bazą bez frameworka, większość pracy wymagałaby pisania SQL (obcy język do baz danych).

Przykład tworzenia tabeli w SQL:

```sql
CREATE TABLE movies (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    year INTEGER
);
```

---

## „Klasyczne" zarządzanie bazami danych

Taki kod trzeba:
- przetestować i sprawdzić,
- zapisać gdzieś bezpiecznie,
- pamiętać o wykonaniu go na każdej maszynie.

To jest podatne na błędy.

---

## Tworzenie modelu w Django

Django pozwala definiować strukturę bazy jako klasy w Pythonie — to dużo bardziej naturalne.

Otwieramy plik `movies/models.py`:

```bash
nano movies/models.py
```

---

## Tworzenie modelu w Django

W tym pliku tworzymy klasę reprezentującą film:

```python
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()

    def __str__(self):
        return self.title
```

---

## Tworzenie modelu w Django

Zapisujemy plik. Teraz Django wie, co powinno być w bazie danych.

Generujemy migrację (przepis na zmianę bazy):

```bash
python manage.py makemigrations
```

---

## Tworzenie modelu w Django

Jeśli chcemy zobaczyć co zostanie wykonane, bez faktycznego wykonania:

```bash
python manage.py sqlmigrate movies 0001
```

To pokaże nam wygenerowany SQL — możemy sprawdzić, co dokładnie Django planuje zrobić.

---

## Wykonanie migracji

Aby faktycznie zastosować migrację do bazy:

```bash
python manage.py migrate
```

Po tym poleceniu tabela `Movie` będzie już w bazie danych.

---

## Rejestracja modelu w admin

Django posiada wbudowany panel administracyjny — żeby on wiedział o naszym modelu, musimy go tam zarejestrować.

Otwieramy `movies/admin.py`:

```bash
nano movies/admin.py
```

---

## Rejestracja modelu w admin

Dopisujemy rejestrację:

```python
from django.contrib import admin
from .models import Movie


admin.site.register(Movie)
```

---

## Rejestracja modelu w admin

Zapisujemy i wracamy na [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

Powinna się pojawić opcja dodawania filmów.

Można teraz wpisać kilka filmów, żeby mieć dane do pracy.

---

## Wyświetlanie danych z bazy w szablonie

Teraz pobieramy filmy z bazy i pokazujemy je na stronie.

Wracamy do `movies/views.py`:

```bash
nano movies/views.py
```

---

## Wyświetlanie danych z bazy w szablonie

Modyfikujemy widok:

```python
from django.shortcuts import render
from .models import Movie


def hello_world(request):
    movies = Movie.objects.all()
    context = {"movies": movies}
    return render(request, template_name="hello.html", context=context)
```

---

## Wyświetlanie danych z bazy w szablonie

Otwieramy `movies/templates/hello.html`:

```bash
nano movies/templates/hello.html
```

---

## Wyświetlanie danych z bazy w szablonie

Teraz przystępujemy dane do szablonu — używając **pętli** w szablonie:

```django
<h1>Filmy w bazie:</h1>
<ul>
    {% for movie in movies %}
        <li>{{ movie.title }} ({{ movie.year }})</li>
    {% endfor %}
</ul>
```

---

## Wyświetlanie danych z bazy w szablonie

Odświeżamy stronę [http://127.0.0.1:8000/hello/](http://127.0.0.1:8000/hello/).

Powinna się pojawić lista filmów, które dodaliśmy przez panel administracyjny.

---

## Jak włączyć obsługę Django w PyCharm? (opcjonalnie)

Jeśli używasz PyCharm Professional (nie Community), możesz aktywować wsparcie dla Django:

- Otwórz PyCharm
- Otwórz katalog projektu
- Wejdź w **Preferences** (macOS: `Cmd+,`) lub **Settings** (Windows/Linux: `Ctrl+Alt+S`)

---

## Jak włączyć obsługę Django w PyCharm? (opcjonalnie)

- Szukaj **Django Support**
- Zaznacz **Enable Django Support**
- W polu **Django project root** wskaż katalog projektu (tam gdzie `manage.py`)
- W polu **Settings** wskaż `goodmovies/settings.py`

---

## Jak włączyć obsługę Django w PyCharm? (opcjonalnie)

Po włączeniu:
- PyCharm będzie lepiej rozumieć strukturę projektu
- Będzie auto-complete dla Django komend
- Będzie linting dla Django kodu

Ale to jest całkowicie opcjonalne — terminal + `nano` wystarczy zawsze.

---

## Zadanie

Sprawdź, czy zalogowany użytkownik to admin (superuser).

Podpowiedź: w szablonie możesz użyć `{{ request.user.is_superuser }}` lub `{{ request.user.is_staff }}`.

Spróbuj zalogować się jako superuser (przez admin) i zobaczyć czy wartość się zmienia.

