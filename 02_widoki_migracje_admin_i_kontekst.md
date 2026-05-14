# 02 Widoki, migracje, admin i kontekst
*[Mikołaj Leszczuk](mailto:mikolaj.leszczuk@agh.edu.pl), [Agnieszka Rudnicka](mailto:rudnicka@agh.edu.pl)*

* Start i tryb pracy
* Nasza pierwsza aplikacja
* Nasz pierwszy widok i automatyczne przeładowanie aplikacji
* Nasz pierwszy „pełnoprawny” widok
* Bazy danych i migracja bazy danych
* Tworzenie super-użytkownika
* Panel administracyjny
* Kontekst w szablonach HTML

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
- Alternatywnie: IDE (PyCharm/VS Code), konfiguracja będzie pokazana w lekcji 03

---

## Nasza pierwsza aplikacja

W środowisku Django przyjęło się, że jeden projekt składa się z wielu mniejszych aplikacji (*apps*).

Każda z nich odpowiada za konkretną funkcjonalność i — przynajmniej w założeniu — powinna być możliwie niezależna od pozostałych.

---

## Nasza pierwsza aplikacja

Stwórzmy więc pierwszą aplikację. Na potrzeby kursu będziemy tworzyć mini-bibliotekę zawierającą filmy.

```bash
python manage.py startapp movies
```

---

## Nasza pierwsza aplikacja

Po utworzeniu aplikacji warto sprawdzić jej strukturę.

UNIX:

```bash
tree movies
```

Windows:

```bash
tree /F movies
```

---

## Nasza pierwsza aplikacja

W katalogu `movies/` pojawiły się między innymi:

* `migrations/` — pliki migracji bazodanowych
* `admin.py` — konfiguracja panelu administracyjnego
* `apps.py` — podstawowe informacje o aplikacji

---

## Nasza pierwsza aplikacja

Dalej znajdziemy też:

* `models.py` — definicje modeli danych
* `tests.py` — testy
* `views.py` — widoki aplikacji

To właśnie od `views.py` zaczniemy.

---

## Nasz pierwszy widok i automatyczne przeładowanie aplikacji

Otwórzmy plik `movies/views.py` w `nano`:

```bash
nano movies/views.py
```

Na początek posłużymy się prostą funkcją, która przyjmuje żądanie HTTP i zwraca prostą odpowiedź tekstową.

---

## Nasz pierwszy widok i automatyczne przeładowanie aplikacji

Na górze pliku dodajmy import:

```python
from django.http import HttpResponse
```

---

## Nasz pierwszy widok i automatyczne przeładowanie aplikacji

Następnie napiszmy prosty widok:

```python
def hello_world(request):
    return HttpResponse("Witaj świecie!")
```

---

## Nasz pierwszy widok i automatyczne przeładowanie aplikacji

Cały plik `movies/views.py` może wyglądać tak:

```python
from django.http import HttpResponse


# Create your views here.
def hello_world(request):
    return HttpResponse("Witaj świecie!")
```

---

## Nasz pierwszy widok i automatyczne przeładowanie aplikacji

To jednak jeszcze nie wystarczy.

Jeśli wejdziemy na [http://127.0.0.1:8000/](http://127.0.0.1:8000/), nie zobaczymy naszego napisu, bo aplikacja `movies` nie została jeszcze dołączona do projektu.

---

## Nasz pierwszy widok i automatyczne przeładowanie aplikacji

Otwórzmy plik `goodmovies/settings.py` i odszukajmy listę `INSTALLED_APPS`:

```bash
nano goodmovies/settings.py
```

Dopisujemy tam naszą aplikację:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "movies",
]
```

---

## Nasz pierwszy widok i automatyczne przeładowanie aplikacji

Teraz trzeba jeszcze podpiąć widok pod konkretny adres URL.

Otwórzmy `goodmovies/urls.py` i dopiszmy import oraz nową ścieżkę:

```bash
nano goodmovies/urls.py
```

```python
from django.contrib import admin
from django.urls import path

from movies import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hello/", views.hello_world),
]
```

---

## Nasz pierwszy widok i automatyczne przeładowanie aplikacji

Teraz możemy wejść pod adres:

[http://127.0.0.1:8000/hello/](http://127.0.0.1:8000/hello/)

Powinniśmy zobaczyć prostą odpowiedź tekstową.

---

## Nasz pierwszy widok i automatyczne przeładowanie aplikacji

Jeśli serwer był uruchomiony podczas edycji plików, w terminalu mogliśmy zauważyć automatyczne przeładowanie aplikacji.

Przykładowy komunikat wygląda mniej więcej tak:

```bash
.../views.py changed, reloading.
Performing system checks...
Watching for file changes with StatReloader
```

---

## Nasz pierwszy widok i automatyczne przeładowanie aplikacji

To domyślny mechanizm deweloperski Django.

Nasłuchuje on zmian w plikach projektu i dzięki temu nie musimy ręcznie restartować serwera po każdej modyfikacji kodu Pythona.

---

## Nasz pierwszy „pełnoprawny” widok

Dotychczasowy widok zwracał zwykły tekst.

Tym razem spróbujmy zwrócić odpowiedź HTML, czyli wyrenderować szablon.

---

## Nasz pierwszy „pełnoprawny” widok

Wracamy do pliku `movies/views.py` i zmieniamy funkcję `hello_world`:

Usuwamy też niepotrzebny już import `HttpResponse`.

```python
from django.shortcuts import render


# Create your views here.
def hello_world(request):
    return render(request, template_name="hello.html")
```

---

## Nasz pierwszy „pełnoprawny” widok

Funkcja `render()` przyjmuje tutaj dwa wymagane argumenty:

* `request` — przychodzące żądanie
* `template_name` — nazwę szablonu HTML

Później dojdzie jeszcze trzeci ważny element: kontekst.

---

## Nasz pierwszy „pełnoprawny” widok

Musimy teraz utworzyć szablon `hello.html`.

W aplikacji `movies` tworzymy katalog `templates/`, a w nim plik `hello.html`.

Końcowa ścieżka powinna wyglądać tak:

```text
movies/templates/hello.html
```

---

## Nasz pierwszy „pełnoprawny” widok

W pliku `movies/templates/hello.html` wpiszmy na przykład:

```html
<h1>Witaj świecie</h1>
```

---

## Nasz pierwszy „pełnoprawny” widok

Po odświeżeniu strony [http://127.0.0.1:8000/hello/](http://127.0.0.1:8000/hello/) powinniśmy zobaczyć napis, ale tym razem już jako nagłówek HTML `<h1>`.

---

## Bazy danych i migracja bazy danych

Wróćmy na chwilę do pliku `goodmovies/settings.py`.

To tutaj znajdują się kluczowe ustawienia projektu, w tym konfiguracja bazy danych.

---

## Bazy danych i migracja bazy danych

Domyślna konfiguracja wygląda mniej więcej tak:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

---

## Bazy danych i migracja bazy danych

Po utworzeniu projektu w katalogu głównym pojawia się plik `db.sqlite3`.

To właśnie nasza baza danych w formacie SQLite.

Sprawdzić można komendą `tree` — wśród plików projektowych pojawi się `db.sqlite3`:

```bash
tree
```

Na potrzeby kursu zostajemy przy SQLite — jest proste w obsłudze i nie wymaga instalowania dodatkowego serwera baz danych.

---

## Bazy danych i migracja bazy danych

Podczas uruchamiania projektu mogliśmy zauważyć komunikat o niezaaplikowanych migracjach:

```bash
System check identified no issues (0 silenced).

You have ... unapplied migration(s). Your project may not work properly until you apply them.
Run 'python manage.py migrate' to apply them.
```

---

## Bazy danych i migracja bazy danych

W skrócie oznacza to, że stan bazy danych nie odpowiada jeszcze temu, czego oczekuje aplikacja.

Na przykład wbudowany model użytkownika Django powinien mieć odpowiednie tabele w bazie — a na razie ich jeszcze nie ma.

---

## Bazy danych i migracja bazy danych

Żeby przygotować bazę danych, uruchamiamy migracje:

```bash
python manage.py migrate
```

---

## Bazy danych i migracja bazy danych

Po wykonaniu migracji Django utworzy potrzebne tabele, między innymi na użytkowników, sesje i uprawnienia.

Od tej chwili projekt jest gotowy do pracy z panelem administracyjnym.

---

## Tworzenie super-użytkownika

Aby zalogować się do panelu administracyjnego, potrzebujemy konta z odpowiednimi uprawnieniami.

Tworzymy je poleceniem:

```bash
python manage.py createsuperuser
```

---

## Tworzenie super-użytkownika

Django poprosi nas kolejno o:

* nazwę użytkownika,
* adres e-mail,
* hasło.

Po zakończeniu będziemy mogli zalogować się do panelu admina.

---

## Panel administracyjny

Przejdźmy na stronę:

[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Panel administracyjny

Można tu między innymi zarządzać użytkownikami.

Wszystkie widoki panelu administracyjnego, które na razie oglądamy, są generowane automatycznie przez Django.

---

## Panel administracyjny

Na kolejnych zajęciach dodamy własne modele i podepniemy je pod panel administracyjny.

Na razie zalogujmy się, rozejrzyjmy po interfejsie i na końcu się wylogujmy.

---

## Kontekst w szablonach HTML

Wróćmy do przykładu z `hello.html`.

Gdybyśmy chcieli wyświetlić informację o aktualnie zalogowanym użytkowniku, możemy w szablonie użyć zmiennej dostępnej domyślnie w kontekście:

```django
<p>
    Aktualny użytkownik to: {{ request.user }}
</p>
```

---

## Kontekst w szablonach HTML

W przeglądarce zobaczymy na przykład:

```text
Aktualny użytkownik to: AnonymousUser
```

A jeśli zalogujemy się przez panel admina, zamiast `AnonymousUser` pojawi się login naszego użytkownika.

---

## Kontekst w szablonach HTML

Za pomocą `{{ zmienna }}` możemy wypisywać dane dostępne w kontekście szablonu.

Można myśleć o kontekście jak o słowniku: pod każdym kluczem kryje się jakaś wartość, którą szablon potrafi wyświetlić.

---

## Kontekst w szablonach HTML

Możemy też przekazać do szablonu własne dane.

Załóżmy, że chcemy dodać aktualną datę i godzinę.

Wracamy do `movies/views.py`:

```python
from datetime import datetime

from django.shortcuts import render


# Create your views here.
def hello_world(request):
    our_context = {"time": datetime.now()}
    return render(
        request,
        template_name="hello.html",
        context=our_context,
    )
```

---

## Kontekst w szablonach HTML

W powyższym kodzie tworzymy słownik `our_context`, a następnie przekazujemy go jako `context` do funkcji `render()`.

Dzięki temu dane ze słownika stają się dostępne w szablonie HTML.

---

## Kontekst w szablonach HTML

W `movies/templates/hello.html` możemy teraz dopisać:

Najpierw zaraz edytujemy szablon:

```bash
nano movies/templates/hello.html
```

I dodajemy:

```django
<p>
    Aktualny czas: {{ time }}
</p>
```

Następnie odświeżamy stronę w przeglądarce [http://127.0.0.1:8000/hello/](http://127.0.0.1:8000/hello/) — powinna się pojawić aktualna godzina i minuta.

---

## Kontekst w szablonach HTML

To właśnie przez kontekst przekazujemy informacje z backendu do frontendu.

Później będą to na przykład dane odczytane z bazy: filmy, recenzje, reżyserzy i inne obiekty naszej aplikacji.

