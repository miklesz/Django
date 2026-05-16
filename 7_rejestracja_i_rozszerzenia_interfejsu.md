# 7 Rejestracja i rozszerzenia interfejsu
*[Mikołaj Leszczuk](mailto:mikolaj.leszczuk@agh.edu.pl), [Agnieszka Rudnicka](mailto:rudnicka@agh.edu.pl)*

* Start każdych zajęć
* System rejestracji użytkowników
* Formularze
* Szablony autoryzacji

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

## Rejestracja użytkowników

Implementujemy system rejestracji nowych użytkowników.

Django oferuje gotowy formularz `UserCreationForm` dla tego celu.

---

## Widok rejestracji

W [`movies/views.py`](http://localhost:8888/edit/movies/views.py):

```python
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(
        request,
        'registration/signup.html',
        {'form': form}
    )
```

---

## Dlaczego sprawdzamy `request.method == "POST"`?

HTTP ma różne metody:
- `GET` — pobranie strony (wyświetlenie formularza)
- `POST` — wysłanie danych (przetworzenie formularza)

Zazwyczaj:
- `GET` → wyświetlujemy pusty formularz
- `POST` → przetwarzamy dane i zapisujemy użytkownika

---

## Szablon rejestracji

Tworzymy `movies/templates/registration/signup.html`:

```django
{% extends 'base.html' %}

{% block content %}
<h1>Rejestracja</h1>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Zarejestruj się</button>
</form>

<p>Masz już konto? <a href="{% url 'login' %}">Zaloguj się</a></p>
{% endblock %}
```

---

## Token CSRF

`{% csrf_token %}` to bezpieczeństwo Django — chroni przed atakami CSRF (Cross-Site Request Forgery).

Musi być w każdym formularzu wysyłającym dane POST.

---

## Szablon logowania

Tworzymy `movies/templates/registration/login.html`:

```django
{% extends 'base.html' %}

{% block content %}
<h1>Logowanie</h1>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Zaloguj się</button>
</form>

<p>Nie masz konta? <a href="{% url 'signup' %}">Zarejestruj się</a></p>
{% endblock %}
```

---

## Szablon wylogowania

Tworzymy `movies/templates/registration/logged_out.html`:

```django
{% extends 'base.html' %}

{% block content %}
<h1>Wylogowano</h1>

<p>Zostałeś wylogowany.</p>
<p><a href="{% url 'login' %}">Zaloguj się ponownie</a></p>
{% endblock %}
```

---

## Rejestracja URL

W [`goodmovies/urls.py`](http://localhost:8888/edit/goodmovies/urls.py):

```python
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from movies.views import user_signup

urlpatterns = [
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/signup/', user_signup, name='signup'),
]
```

---

## Sprawdzanie autoryzacji w szablonach

W szablonach możemy sprawdzić, czy użytkownik jest zalogowany:

```django
{% if user.is_authenticated %}
    <p>Cześć, {{ user.username }}!</p>
    <a href="{% url 'logout' %}">Wyloguj się</a>
{% else %}
    <a href="{% url 'login' %}">Zaloguj się</a>
{% endif %}
```

---

## Chronimy widoki przed dostępem

Używamy dekoratora `@login_required`:

```python
from django.contrib.auth.decorators import login_required

@login_required
def user_profile(request):
    return render(request, 'profile.html')
```

Teraz tylko zalogowani użytkownicy mogą odwiedzić tę stronę.

---

## Dalsze kroki

1. Dodaj formularze do edycji profilu użytkownika
2. Rozszerz system uprawnień (permissions, groups)
3. Dodaj możliwość dodawania recenzji tylko dla zalogowanych
4. Zaimplementuj funkcjonalność „reset hasła"
5. Dodaj potwierdzenie emaila przy rejestracji
