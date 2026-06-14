# 7 Użytkownicy aplikacji
*[Mikołaj Leszczuk](mailto:mikolaj.leszczuk@agh.edu.pl), [Agnieszka Rudnicka](mailto:rudnicka@agh.edu.pl)*

* Start i punkt wyjścia
* Wbudowane widoki logowania Django
* Profil zalogowanego użytkownika
* Rejestracja przez `UserCreationForm`
* Wylogowanie i nawigacja użytkownika
* Ochrona widoków

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

Mamy już filmy, reżyserów, recenzje i linki między stronami.

Do tej pory zwykły użytkownik nie ma własnego konta w aplikacji.

Na tych zajęciach dodamy logowanie, profil, rejestrację i wylogowanie.

---

## Uwierzytelnianie w Django

Django ma wbudowany system użytkowników.

Korzystaliśmy już z niego pośrednio przy panelu administratora.

Teraz użyjemy go dla zwykłych stron aplikacji:

- logowanie,
- wylogowanie,
- profil,
- rejestracja nowego użytkownika.

---

## Sprawdzenie konfiguracji

Otwieramy `goodmovies/settings.py`:

```bash
nano goodmovies/settings.py
```

Sprawdzamy, czy w `INSTALLED_APPS` są:

```python
"django.contrib.auth",
"django.contrib.contenttypes",
"django.contrib.sessions",
```

Jeśli panel admina działał, te elementy zwykle już są poprawnie ustawione.

---

## Sprawdzenie konfiguracji

W tym samym pliku sprawdzamy `MIDDLEWARE`.

Powinny tam być między innymi:

```python
"django.contrib.sessions.middleware.SessionMiddleware",
"django.contrib.auth.middleware.AuthenticationMiddleware",
```

`SessionMiddleware` pamięta sesję przeglądarki.

`AuthenticationMiddleware` udostępnia `request.user`.

---

## Wbudowane URL-e auth

Django dostarcza gotowe widoki logowania, wylogowania i zmiany hasła.

Podłączymy je przez `include`.

Otwieramy `goodmovies/urls.py`:

```bash
nano goodmovies/urls.py
```

---

## Podłączenie URL-i auth

Na górze pliku importujemy `include`:

```python
from django.urls import include, path
```

Do `urlpatterns` dodajemy:

```python
path("accounts/", include("django.contrib.auth.urls")),
```

To doda między innymi `/accounts/login/` i `/accounts/logout/`.

---

## Co robi `include`?

`include` dołącza zestaw adresów z innego modułu.

Nie musimy osobno pisać ścieżek do logowania i wylogowania.

Django dostarcza te widoki w `django.contrib.auth.urls`.

My musimy przygotować szablony HTML.

---

## Szablon logowania

Tworzymy katalog i plik:

```bash
mkdir -p movies/templates/registration
nano movies/templates/registration/login.html
```

Django szuka szablonu logowania właśnie pod nazwą `registration/login.html`.

---

## `login.html`

```django
{% extends "base.html" %}

{% block content %}
  <h2>Logowanie</h2>

  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Zaloguj się</button>
  </form>
{% endblock %}
```

Za chwilę wyjaśnimy:

- skąd bierze się zmienna `form`,
- po co jest `{% csrf_token %}`,
- co robi `form.as_p`,
- dlaczego link do rejestracji dodamy dopiero później.

---

## Token CSRF

Tag `csrf_token` jest wymagany w formularzach wysyłanych metodą POST.

Chroni przed atakiem CSRF, czyli podszyciem się pod formularz z innej strony.

Jeśli go zabraknie, Django odrzuci wysłanie formularza.

---

## Sprawdzenie logowania

Uruchamiamy serwer:

```bash
python manage.py runserver
```

Wchodzimy na:

[http://127.0.0.1:8000/accounts/login/](http://127.0.0.1:8000/accounts/login/)

Na tym etapie sprawdzamy, czy formularz logowania się wyświetla.

Nie musimy jeszcze kończyć logowania.

Pełny test zrobimy po utworzeniu strony profilu.

Jeśli ktoś zaloguje się teraz i zobaczy `404` na `/accounts/profile/`, to jest spodziewane.

---

## Gdy nie pamiętamy hasła

Jeśli znamy nazwę użytkownika, ustawiamy nowe hasło:

```bash
python manage.py changepassword NAZWA_UZYTKOWNIKA
```

Starego hasła nie da się podejrzeć.

Jeśli nie pamiętamy nazwy użytkownika, na potrzeby kursu tworzymy nowego superusera:

```bash
python manage.py createsuperuser
```

Nazwa użytkownika musi być nowa, ale e-mail nie musi być unikalny.

---

## Profil użytkownika

Po zalogowaniu Django domyślnie próbuje przejść na `/accounts/profile/`.

Dodamy więc taką stronę.

Najpierw widok, potem URL, potem szablon.

---

## Widok profilu

Otwieramy `movies/views.py`:

```bash
nano movies/views.py
```

Dodajemy import:

```python
from django.contrib.auth.decorators import login_required
```

Za chwilę wyjaśnimy, czym są dekoratory w Pythonie i po co przy widoku pojawi się znak `@`.

---

## Czym jest dekorator?

Dekorator to sposób Pythona na dodanie zachowania do funkcji.

Zapis z `@` stawiamy nad funkcją:

```python
@login_required
def profile_view(request):
    ...
```

Czytamy to praktycznie tak:

```text
zanim uruchomisz ten widok, sprawdź logowanie użytkownika
```

---

## Widok profilu

Dopisujemy widok:

```python
@login_required
def profile_view(request):
    return render(request, "profile.html")
```

`@login_required` oznacza, że strona jest dostępna tylko po zalogowaniu.

Jeśli użytkownik nie jest zalogowany, Django nie uruchomi widoku od razu.

Najpierw przekieruje go do logowania.

---

## URL profilu

Otwieramy `goodmovies/urls.py`:

```bash
nano goodmovies/urls.py
```

Dodajemy:

```python
path("accounts/profile/", views.profile_view, name="user-profile"),
```

Ten adres pasuje do domyślnego zachowania Django po logowaniu.

---

## Szablon profilu

Tworzymy plik:

```bash
nano movies/templates/profile.html
```

Django udostępnia aktualnego użytkownika jako `request.user`.

---

## `profile.html`

```django
{% extends "base.html" %}

{% block content %}
  <h2>Profil</h2>

  <p>Użytkownik: {{ request.user.username }}</p>
  <p>Ostatnie logowanie: {{ request.user.last_login }}</p>

  <form method="post" action="{% url 'logout' %}">
    {% csrf_token %}
    <button type="submit">Wyloguj się</button>
  </form>
{% endblock %}
```

Wylogowanie robimy formularzem POST, nie zwykłym linkiem.

Na kolejnym slajdzie rozbijemy ten szablon na najważniejsze elementy.

---

## Co robi `profile.html`?

`request.user` to aktualnie zalogowany użytkownik.

`request.user.username` pokazuje jego nazwę.

`request.user.last_login` pokazuje ostatnie logowanie.

`{% url 'logout' %}` wyznacza adres widoku wylogowania.

Formularz wylogowania musi mieć `method="post"` i `{% csrf_token %}`.

---

## Przekierowanie po logowaniu

Jeśli chcemy jawnie ustawić stronę po zalogowaniu, edytujemy `goodmovies/settings.py`:

```bash
nano goodmovies/settings.py
```

Na końcu dodajemy:

```python
LOGIN_REDIRECT_URL = "/accounts/profile/"
```

---

## Sprawdzenie profilu

Wchodzimy na:

[http://127.0.0.1:8000/accounts/login/](http://127.0.0.1:8000/accounts/login/)

Logujemy się.

Po zalogowaniu powinniśmy zobaczyć profil użytkownika.

Sprawdzamy też przycisk wylogowania.

---

## Rejestracja użytkowników

Logowanie działa dla istniejących kont.

Teraz dodamy rejestrację nowych użytkowników.

Użyjemy gotowego formularza Django:

```python
UserCreationForm
```

Na kolejnych slajdach dodamy URL, widok i szablony.

---

## URL rejestracji

Otwieramy `goodmovies/urls.py`:

```bash
nano goodmovies/urls.py
```

Dodajemy ścieżkę:

```python
path("accounts/signup/", views.user_signup, name="signup"),
```

Najwygodniej dodać ją przed:

```python
path("accounts/", include("django.contrib.auth.urls")),
```

---

## Widok rejestracji

Otwieramy `movies/views.py`:

```bash
nano movies/views.py
```

Dodajemy importy:

```python
from django.contrib.auth.forms import UserCreationForm
```

Jeśli `render` jest już zaimportowany, nie dodajemy go drugi raz.

---

## Widok rejestracji

```python
def user_signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "registration/signup_complete.html")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})
```

Na kolejnym slajdzie wyjaśnimy `GET`, `POST` i formularz.

---

## Co robi ten widok?

`GET` oznacza wejście na stronę i pokazanie pustego formularza.

`POST` oznacza wysłanie wypełnionego formularza.

`UserCreationForm(request.POST)` wczytuje dane z formularza.

`form.is_valid()` sprawdza poprawność danych.

`form.save()` tworzy użytkownika w bazie.

---

## Szablon rejestracji

Tworzymy plik:

```bash
nano movies/templates/registration/signup.html
```

---

## `signup.html`

```django
{% extends "base.html" %}

{% block content %}
  <h2>Rejestracja</h2>

  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Zarejestruj się</button>
  </form>

  <p><a href="{% url 'login' %}">Mam już konto</a></p>
{% endblock %}
```

Na kolejnym slajdzie wyjaśnimy, co jest tu takie samo jak w logowaniu, a co jest nowe.

---

## Co robi `signup.html`?

Mechanika formularza jest taka sama jak przy logowaniu:

- `method="post"` wysyła dane formularza,
- `{% csrf_token %}` chroni wysłanie formularza,
- `{{ form.as_p }}` pokazuje pola formularza.

Nowe jest to, że ten formularz tworzy konto użytkownika.

Link `{% url 'login' %}` prowadzi osoby z istniejącym kontem do logowania.

---

## Szablon po rejestracji

Tworzymy plik:

```bash
nano movies/templates/registration/signup_complete.html
```

Ten szablon pokażemy po poprawnym utworzeniu konta.

---

## `signup_complete.html`

```django
{% extends "base.html" %}

{% block content %}
  <h2>Konto utworzone</h2>

  <p>Możesz się teraz zalogować.</p>
  <p><a href="{% url 'login' %}">Przejdź do logowania</a></p>
{% endblock %}
```

Na kolejnym slajdzie wyjaśnimy, kiedy Django pokazuje ten szablon.

---

## Co robi `signup_complete.html`?

Ten szablon pojawia się po poprawnym utworzeniu konta.

Wracamy do niego z widoku `user_signup` po:

```python
form.save()
```

Użytkownik nie jest jeszcze automatycznie zalogowany.

Dlatego pokazujemy link do strony logowania.

---

## Sprawdzenie rejestracji

Wchodzimy na:

[http://127.0.0.1:8000/accounts/signup/](http://127.0.0.1:8000/accounts/signup/)

Zakładamy nowe konto.

Po poprawnej rejestracji powinniśmy zobaczyć stronę `Konto utworzone`.

Potem logujemy się na nowe konto.

---

## Szablon po wylogowaniu

Django po wylogowaniu szuka szablonu:

```text
registration/logged_out.html
```

Tworzymy plik:

```bash
nano movies/templates/registration/logged_out.html
```

---

## `logged_out.html`

```django
{% extends "base.html" %}

{% block content %}
  <h2>Wylogowano</h2>

  <p>Sesja została zakończona.</p>
  <p><a href="{% url 'login' %}">Zaloguj się ponownie</a></p>
{% endblock %}
```

Na kolejnym slajdzie wyjaśnimy, kiedy Django używa tego szablonu.

---

## Co robi `logged_out.html`?

Ten szablon pokazuje się po poprawnym wylogowaniu.

Korzysta z niego wbudowany widok `logout`.

Tekst potwierdza, że sesja użytkownika została zakończona.

Link `{% url 'login' %}` pozwala od razu zalogować się ponownie.

---

## Jeśli szablon się nie podmienia

To slajd awaryjny.

Objaw: po wylogowaniu widzimy inną stronę niż nasz `logged_out.html`.

Przyczyna: Django mogło wcześniej znaleźć szablon z aplikacji Django.

Django szuka szablonów zgodnie z kolejnością aplikacji w `INSTALLED_APPS`.

---

## Pierwszeństwo szablonów

Otwieramy `goodmovies/settings.py`:

```bash
nano goodmovies/settings.py
```

W `INSTALLED_APPS` dajemy `movies` przed aplikacjami Django:

```python
INSTALLED_APPS = [
    "movies",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
```

Dzięki temu szablony z `movies` mają pierwszeństwo.

---

## Linki użytkownika w `base.html`

Otwieramy szablon bazowy:

```bash
nano movies/templates/base.html
```

Dodamy informację o użytkowniku oraz logowanie i wylogowanie.

---

## Fragment do `base.html`

```django
{% if request.user.is_authenticated %}
  <p>Zalogowany jako {{ request.user.username }}</p>
  <form method="post" action="{% url 'logout' %}">
    {% csrf_token %}
    <button type="submit">Wyloguj się</button>
  </form>
{% else %}
  <p>
    <a href="{% url 'login' %}">Zaloguj się</a>
    |
    <a href="{% url 'signup' %}">Zarejestruj się</a>
  </p>
{% endif %}
```

Ten fragment najlepiej umieścić przed blokiem `content`.

Na kolejnym slajdzie wyjaśnimy, co jest tu nowe.

---

## Co robi fragment w `base.html`?

`base.html` działa na wielu stronach, więc to dobre miejsce na nawigację użytkownika.

`request.user.is_authenticated` sprawdza, czy użytkownik jest zalogowany.

Jeśli jest zalogowany, pokazujemy jego nazwę i przycisk wylogowania.

Jeśli nie jest zalogowany, pokazujemy linki do logowania i rejestracji.

---

## Dlaczego wylogowanie to formularz?

Współczesne Django oczekuje wylogowania metodą POST.

Powód: wylogowanie zmienia stan aplikacji.

Django usuwa dane sesji aktualnego użytkownika.

Zwykły link wysyła żądanie GET, a GET powinien tylko pobierać stronę.

Dlatego przy wylogowaniu używamy:

```django
<form method="post" action="{% url 'logout' %}">
```

i dodajemy tag `csrf_token`, żeby potwierdzić, że formularz pochodzi z naszej strony.

---

## Ochrona innych widoków

Ten sam dekorator możemy użyć przy dowolnym widoku funkcyjnym.

Schemat:

```python
@login_required
def nazwa_widoku(request):
    ...
```

Taki widok będzie dostępny tylko po zalogowaniu.

---

## Sprawdzenie całości

Sprawdzamy po kolei:

1. [http://127.0.0.1:8000/accounts/signup/](http://127.0.0.1:8000/accounts/signup/) - rejestracja.
2. [http://127.0.0.1:8000/accounts/login/](http://127.0.0.1:8000/accounts/login/) - logowanie.
3. [http://127.0.0.1:8000/accounts/profile/](http://127.0.0.1:8000/accounts/profile/) - profil.
4. Przycisk wylogowania.
5. Widok strony po wylogowaniu.

Jeśli coś nie działa, zaczynamy od sprawdzenia `urls.py` i nazw szablonów.

---

## Koniec części obowiązkowej

Jeśli te pięć punktów działa, główny cel ćwiczenia jest zrealizowany.

---

## Zadania opcjonalne

Poniższe zadania rozwijają materiał z ćwiczenia.

---

## Zadanie opcjonalne 1

Dodaj na stronie profilu link do listy filmów.

Użyj nazwy URL `movie-list-v2`.

---

## Rozwiązanie 1

Otwieramy `profile.html`:

```bash
nano movies/templates/profile.html
```

Dopisujemy:

```django
<p><a href="{% url 'movie-list-v2' %}">Przejdź do listy filmów</a></p>
```

Dzięki nazwie URL nie wpisujemy ręcznie `/filmy-v2/`.

Sprawdzamy:

[http://127.0.0.1:8000/accounts/profile/](http://127.0.0.1:8000/accounts/profile/)

---

## Zadanie opcjonalne 2

Zabezpiecz widok `list_movies` dekoratorem `@login_required`.

Po zmianie lista pod adresem `/filmy/` będzie dostępna tylko po zalogowaniu.

---

## Rozwiązanie 2

Otwieramy `movies/views.py`:

```bash
nano movies/views.py
```

Dopisujemy dekorator nad funkcją `list_movies`:

```python
from django.contrib.auth.decorators import login_required


@login_required
def list_movies(request):
    movies = Movie.objects.all()
    return render(request, "movie_list.html", {"movies": movies})
```

Niezalogowany użytkownik zostanie przekierowany na `/accounts/login/`.

Sprawdzamy:

[http://127.0.0.1:8000/filmy/](http://127.0.0.1:8000/filmy/)

---

## Podsumowanie kursu

W trakcie kursu zbudowaliśmy aplikację `goodmovies`.

Po drodze pojawiły się:

- projekt i aplikacja Django,
- modele, migracje i baza SQLite,
- panel administratora,
- widoki funkcyjne i klasowe,
- szablony HTML i dziedziczenie z `base.html`,
- relacje między filmami, reżyserami i recenzjami,
- linkowanie stron po nazwach URL,
- logowanie, wylogowanie, profil i rejestracja użytkownika.

---

## Co warto zapamiętać

W większości prostych zmian w Django wracamy do tej samej mapy:

```text
model -> widok -> szablon -> URL
```

Jeśli strona się nie otwiera, najpierw sprawdzamy:

1. czy URL istnieje w `urls.py`,
2. czy widok zwraca właściwy szablon,
3. czy nazwa szablonu zgadza się z plikiem,
4. czy dane są przekazane w kontekście.

---

## Co dalej

Naturalne rozszerzenia tej aplikacji to:

- formularz dodawania filmu przez stronę,
- edycja i usuwanie filmów,
- recenzje dodawane przez zalogowanych użytkowników,
- uprawnienia, czyli kto może zmieniać dane,
- proste testy widoków i modeli,
- publikacja aplikacji poza komputerem lokalnym.

---

## Kontakt i materiały

Materiały z kursu to pliki Markdown od `1_...md` do `7_...md`.

Kod ćwiczeniowy jest w Waszych własnych katalogach projektowych.

Kontakt:

- [Mikołaj Leszczuk](mailto:mikolaj.leszczuk@agh.edu.pl)
- [Agnieszka Rudnicka](mailto:rudnicka@agh.edu.pl)

---

## Dziękujemy

Dziękujemy za udział w kursie.

Macie już działający projekt Django i podstawy do dalszej samodzielnej pracy.
