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

Po aktywacji używamy poleceń typu `python manage.py runserver`.

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

## `include("django.contrib.auth.urls")`

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

  <p><a href="{% url 'signup' %}">Zarejestruj się</a></p>
{% endblock %}
```

---

## Token CSRF

`{% csrf_token %}` jest wymagany w formularzach wysyłanych metodą POST.

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

Jeśli nie pamiętamy hasła, ustawiamy nowe:

```bash
python manage.py changepassword NAZWA_UZYTKOWNIKA
```

Starego hasła nie da się podejrzeć.

Jeśli nie pamiętamy nazwy użytkownika, na potrzeby kursu można utworzyć nowego superusera:

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

---

## Widok profilu

Dopisujemy widok:

```python
@login_required
def profile_view(request):
    return render(request, "profile.html")
```

`@login_required` oznacza, że strona jest dostępna tylko po zalogowaniu.

Niezalogowany użytkownik zostanie przekierowany do logowania.

---

## URL profilu

W `goodmovies/urls.py` dodajemy:

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

W `goodmovies/urls.py` dodajemy ścieżkę:

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

---

## Jeśli szablon się nie podmienia

Jeśli Django nie używa naszego `logged_out.html`, sprawdzamy kolejność aplikacji w `INSTALLED_APPS`.

Najprościej dać `movies` przed aplikacjami Django:

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

Ten fragment najlepiej umieścić przed `{% block content %}`.

---

## Dlaczego wylogowanie to formularz?

Współczesne Django oczekuje wylogowania metodą POST.

Zwykły link wysyła żądanie GET.

Dlatego przy wylogowaniu używamy:

```django
<form method="post" action="{% url 'logout' %}">
```

i dodajemy `{% csrf_token %}`.

---

## Ochrona innych widoków

Ten sam dekorator możemy użyć przy dowolnym widoku funkcyjnym.

Przykład:

```python
@login_required
def first_movie(request):
    movie = Movie.objects.first()
    return render(request, "first_movie.html", {"movie": movie})
```

Taki widok będzie dostępny tylko po zalogowaniu.

---

## Sprawdzenie całości

Sprawdzamy po kolei:

1. `/accounts/signup/` - rejestracja.
2. `/accounts/login/` - logowanie.
3. `/accounts/profile/` - profil.
4. Przycisk wylogowania.
5. Widok strony po wylogowaniu.

Jeśli coś nie działa, zaczynamy od sprawdzenia `urls.py` i nazw szablonów.

---

## Zadanie opcjonalne 1

Dodaj na stronie profilu link do listy filmów.

Użyj nazwy URL `movie-list-v2`.

---

## Rozwiązanie 1

W `profile.html` można dopisać:

```django
<p><a href="{% url 'movie-list-v2' %}">Przejdź do listy filmów</a></p>
```

Dzięki nazwie URL nie wpisujemy ręcznie `/filmy-v2/`.

---

## Zadanie opcjonalne 2

Zabezpiecz widok `first_movie` dekoratorem `@login_required`.

Jeśli nie masz tego widoku w projekcie, potraktuj zadanie jako przykład dla prowadzącego.

---

## Rozwiązanie 2

W `movies/views.py`:

```python
from django.contrib.auth.decorators import login_required


@login_required
def first_movie(request):
    movie = Movie.objects.first()
    return render(request, "first_movie.html", {"movie": movie})
```

Niezalogowany użytkownik zostanie przekierowany na `/accounts/login/`.
