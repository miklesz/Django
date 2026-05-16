# 1 Fundamenty i start aplikacji
*[Mikołaj Leszczuk](mailto:mikolaj.leszczuk@agh.edu.pl), [Agnieszka Rudnicka](mailto:rudnicka@agh.edu.pl)*

* Start i wymagania wstępne
* Czym jest Django?
* Architektura Django: MVC vs. MVT
* Narzędzia pomocnicze i IDE
* Przygotowanie środowiska
* Nasz pierwszy projekt w Django

---

## Start lekcji 1 (jednorazowy setup)

Na tych zajęciach dopiero zakładamy katalog kursowy i środowisko wirtualne, więc nie robimy jeszcze "rytuału startowego" z kolejnych lekcji.

W praktyce dzisiaj:

- tworzymy stały katalog kursowy,
- tworzymy i aktywujemy `venv`,
- uruchamiamy pierwszy projekt Django.

Od lekcji 2 na początku wracamy do katalogu projektu i aktywujemy środowisko.

---

## Wymagania na start: co musimy mieć przed pierwszą komendą

Zanim przejdziemy do Django, potrzebujemy trzech rzeczy:

- działającego terminala,
- zainstalowanego Python 3,
- na Windowsie opcjonalnie: WSL jako wygodnego środowiska Linux.

To są jednorazowe przygotowania, które później mocno upraszczają pracę.

---

## Terminal: jak uruchomić

- **macOS**: `Cmd + Spacja` i wpisz `Terminal`
- **Linux**: uruchom `Terminal` z menu aplikacji
- **Windows**: `Windows Terminal` lub `PowerShell`

W dalszej części lekcji wszystkie polecenia wpisujemy właśnie w terminalu.

---

## Python 3: instalacja i szybka weryfikacja

Jeżeli Python 3 nie jest dostępny, instalujemy go:

- **macOS**: `brew install python`
- **Ubuntu/Debian**: `sudo apt install python3 python3-venv python3-pip`
- **Windows**: instalator z [python.org](https://www.python.org/downloads/) (zaznacz `Add python.exe to PATH`)

Po instalacji sprawdzamy wersję:

```bash
# macOS/Linux/WSL
python3 --version

# Windows PowerShell
py -3 --version
```

---

## WSL na Windows (opcjonalnie, ale polecane)

Jeżeli pracujesz na Windowsie i chcesz mieć środowisko zgodne z Linuxem:

1. Otwórz PowerShell jako Administrator
2. Wykonaj `wsl --install`
3. Zrestartuj komputer
4. Po restarcie dokończ konfigurację Ubuntu i ustaw użytkownika

WSL jest fallbackiem, jeśli natrafisz na różnice między poleceniami windowsowymi i unixowymi.

---

## Tryb pracy na zajęciach

Pracujemy w modelu: **prezentacja + terminal** lub **IDE**.

- Prezentacja: plik HTML lekcji
- Komendy: systemowy terminal
- Domyślnie: terminal + `nano`
- Szybki podgląd: `cat`
- **Alternatywnie: IDE (PyCharm/VS Code)** — konfiguracja opisana poniżej w sekcji _Zintegrowane Środowiska Programistyczne_

Na tym etapie wszystkie ćwiczenia można wykonywać zarówno z terminala jak i z IDE.

---

## Opcje środowiska

- macOS
- Linux
- Windows + WSL
- Windows + Linux VM
- Windows + PowerShell (fallback)

Start może być inny zależnie od systemu, ale później pracujemy bardzo podobnie.

---

## Czym jest Django?

**Django** to darmowy i open source'owy framework do budowania aplikacji webowych napisany w Pythonie. Innymi słowy to zestaw narzędzi, który przyśpiesza i ułatwia znacząco proces tworzenia stron.

---

## Czym jest Django?

Gdy tworzymy strony internetowe, wiele elementów się powtarza między projektami. Są to przykładowo mechanizmy tworzenia, zarządzania i uwierzytelniania użytkowników, panel zarządzania treścią czy też mechanizmy wyświetlania i przetwarzania formularzy. Django wychodzi naprzeciw tym powtarzającym się wyzwaniom oferując między innymi:

* gotowy system tworzenia, rejestracji i logowania użytkowników

* gotowy system grup i uprawnień do modeli

* mini-framework do tworzenia i przetwarzania formularzy (`django.contrib.forms`)

---

## Czym jest Django?

* auto-generowany panel administracyjny

* gotowe klasy (Class Based Views) na podstawie których można w kilka linijek kodu tworzyć pełnoprawne widoki CRUD (ang. *Create Read Update Delete*)

* potężny ORM (ang. *Object Relational Mapping*), czyli narzędzie do operowania na danych w bazach danych bez potrzeby użycia SQL (ang. *Structured Query Language*)

* wbudowane mechanizmy cachowania, wysyłania maili

* ...i wiele innych

---

## Architektura Django: MVC vs. MVT

Jeżeli te skróty widzisz pierwszy raz, to spokojnie:

- **MVC** i **MVT** to nazwy sposobu organizacji kodu,
- ich cel jest prosty: oddzielić **dane**, **logikę** i **widok HTML**,
- dzięki temu projekt łatwiej rozwijać i poprawiać.

---

## Architektura Django: MVC vs. MVT

![](https://upload.wikimedia.org/wikipedia/commons/1/19/Mvc-diagram.png)

To jest ogólny schemat MVC, który często zobaczysz w materiałach.

---

## Architektura Django: MVC vs. MVT

Najpierw w 2 zdaniach o **MVC**:

- **Model**: dane i reguły pracy na danych,
- **View**: to, co użytkownik widzi,
- **Controller**: przyjmuje żądanie i decyduje, co zrobić dalej.

---

## Architektura Django: MVC vs. MVT

W Django nazwy są trochę inne (**MVT**):

- **Model (MVT)** = **Model (MVC)**,
- **View (MVT)** działa jak **Controller**,
- **Template (MVT)** to warstwa HTML (czyli „widok” dla użytkownika).

---

## Architektura Django: MVC vs. MVT

Jak to działa w praktyce przy jednym wejściu na stronę:

1. Przeglądarka wysyła request,
2. Django `view` uruchamia logikę,
3. `view` pobiera dane z `model`,
4. `template` składa HTML i Django odsyła odpowiedź.

---

## Narzędzia pomocnicze w pracy z Django

Praca z Django, podobnie jak z innymi frameworkami webowymi, korzysta z różnych narzędzi, które ułatwiają rozwój aplikacji. Oto niektóre z nich, które warto znać zanim zaczniemy pracę z Django:

---

## Narzędzia pomocnicze w pracy z Django

- **Git**: System kontroli wersji, który pozwala na zarządzanie zmianami w kodzie źródłowym i współpracę z innymi programistami. Przydatny do śledzenia historii zmian oraz do pracy zespołowej.

---

## Narzędzia pomocnicze w pracy z Django

- **Virtualenv/venv**: Narzędzia do tworzenia izolowanych środowisk Pythona. Umożliwiają instalację pakietów Pythona w sposób, który nie wpływa na inne projekty lub globalną instalację Pythona. To kluczowe, gdy pracujemy nad wieloma projektami na jednym komputerze.

---

## Narzędzia pomocnicze w pracy z Django

- **PIP**: Menedżer pakietów dla Pythona, który jest używany do instalowania i zarządzania bibliotekami i zależnościami w projektach Pythona, w tym Django.

---

## Narzędzia pomocnicze w pracy z Django

- **Docker**: Platforma do tworzenia, uruchamiania i zarządzania aplikacjami w izolowanych kontenerach. Docker może być używany do tworzenia środowisk, które są jednolite między różnymi maszynami developerskimi i serwerami produkcyjnymi, co minimalizuje "działa u mnie, ale nie działa w produkcji".

---

## Narzędzia pomocnicze w pracy z Django

- **IDEs (Zintegrowane środowisko programistyczne)**: Narzędzia takie jak PyCharm czy VSCode oferują zaawansowane funkcje (auto-uzupełnianie, debugowanie, zarządzanie git), które przyspieszają i uprzyjemniają pracę. Szczegółowa konfiguracja znajduje się w sekcji poniżej.

---

## Narzędzia pomocnicze w pracy z Django

Znajomość tych narzędzi nie tylko pomoże w pracy z Django, ale jest też cenną umiejętnością w pracy programisty/programistki Pythona w ogóle. Każde z tych narzędzi może być przedmiotem osobnej sesji szkoleniowej, ale ich podstawowe zrozumienie jest już bardzo pomocne na starcie pracy z Django.

---

## Zintegrowane Środowiska Programistyczne (IDE)

**IDE** (ang. _Integrated Development Environment_) to zaawansowane narzędzie, które łączy edytor kodu, debugger, zarządzanie plikami i wiele innych funkcji przydatnych do programowania. Zamiast używać osobnych narzędzi do każdego zadania, IDE oferuje wszystko w jednym miejscu.

---

## Zintegrowane Środowiska Programistyczne (IDE)

Kiedy pracujesz z Djangiem i Pythonem, IDE może:

- Automatycznie uzupełniać kod (auto-complete)
- Ułatwiać nawigację po projekcie
- Pokazywać błędy w kodzie na bieżąco
- Integrować się z systemem kontroli wersji (git)
- **Automatycznie wybierać i aktywować virtualne środowisko naszego projektu**

---

## PyCharm

**PyCharm** (dostępne w wersji darmowej _Community_ i płatnej _Professional_) to IDE stworzone specjalnie dla Pythona. Jest szczególnie przydatne do pracy z Django.

---

## PyCharm

Aby włączyć obsługę Django w PyCharm:

1. Otwórz PyCharm i załaduj swój projekt
2. Wejdź do ustawień (`Cmd+,` na macOS lub `Ctrl+Alt+S` na Windowsie/Linuksie)
3. Wyszukaj `Django Support` lub przejdź do `Languages & Frameworks` → `Django`

---

## PyCharm

`Django Support`:

![](https://intellij-support.jetbrains.com/hc/user_images/eVSRccUymV1BCrO57Gjd-w.png)

---

## PyCharm

Następnie ustaw:

- `Enable Django Support` — zaznacz to pole
- `Django project root` — wybierz katalog, w którym znajduje się `manage.py`
- `Settings module` — wstaw `goodmovies/settings.py` (dostosuj do nazwy swojego projektu)

Po włączeniu Django Support zyskujesz:
- Lepsze podpowiedzi dla szablonów Django (`.html`)
- Lepszą nawigację po modelach i widokach
- Możliwość uruchamiania serwera Django bezpośrednio z IDE

---

## Zintegrowane Środowiska Programistyczne (IDE) — VSCode

**VSCode** (Visual Studio Code) to lekki, darmowy edytor od Microsoftu. Może być używany do pracy z Django dzięki rozszerzeniom.

Przydatne rozszerzenia VSCode:
- **Python** — oficjalne rozszerzenie Microsoftu do Pythona
- **Django** — wsparcie dla szablonów i składni Django
- **Pylance** — zaawansowana analiza kodu Python

---

## Przygotowanie środowiska

Na początku tworzymy (lub wybieramy) **własny katalog kursowy**, którego używamy konsekwentnie na wszystkich zajęciach.

To powinien być jeden stały katalog roboczy na cały cykl.

Na początku każdych kolejnych zajęć wracamy właśnie do tego katalogu.

Przykład (ścieżka względna):

```bash
cd moj_katalog_kursowy
```

Od tego miejsca wszystkie polecenia wykonujemy w tym samym katalogu kursowym.

---

## Przygotowanie środowiska

Sprawdźmy, czy mamy poprawnie zainstalowany język Python 3:

```bash
# macOS/Linux/WSL
python3 --version

# Windows PowerShell
py -3 --version
```

Po aktywacji środowiska będziemy już używać po prostu `python`.

---

## Przygotowanie środowiska

### Tworzenie środowiska wirtualnego

Tworzymy lokalne środowisko `.venv`.

```bash
# macOS/Linux/WSL
python3 -m venv .venv

# Windows PowerShell
py -3 -m venv .venv
```

---

## Przygotowanie środowiska

### Aktywacja środowiska wirtualnego

```bash
# macOS/Linux/WSL
source .venv/bin/activate

# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

Po aktywacji w terminalu zwykle widać prefiks `(venv)` albo `(.venv)`.

---

## Przygotowanie środowiska

### Dlaczego `venv`?

To lokalna, odseparowana instalacja Pythona i bibliotek dla tego projektu.
Dzięki temu pakiety z innych projektów nie mieszają się ze sobą.

### Instalowanie bibliotek/zależności

Na wstępie upewnijmy się, że mamy najnowszą wersję `pip`:

```bash
python -m pip install --upgrade pip
```

A teraz właściwa część — instalujemy framework Django:

```bash
python -m pip install Django
```

---

## Przygotowanie środowiska

Po wykonaniu powyższego polecenia możemy sprawdzić aktualnie zainstalowane pakiety poleceniem `pip list`. U mnie lista wygląda tak:

```bash
python -m pip list
```

Dobrą praktyką jest stworzenie pliku z listą zależności wymaganych do uruchomienia projektu. Najprostszą metodą jest wykonanie polecenia:

```bash
python -m pip freeze > requirements.txt
```

Zapisze ono wszystkie biblioteki wraz z dokładnymi ich wersjami do pliku o nazwie `requirements.txt`. Nazwa tego pliku jest pewnego rodzaju konwencją, którą można spotkać w wielu projektach.

---

## Przygotowanie środowiska

Zaglądnijmy do pliku `requirements.txt`:

```bash
cat requirements.txt
```

Lista jest krótsza niż wynik `pip list` — nie ma tu `pip` ani `setuptools`, bo są one częścią samego Pythona i nie zalicza się ich do zależności projektu.

---

## Przygotowanie środowiska

Gdybyśmy chcieli odtworzyć projekt na innym komputerze, wystarczy:

```bash
python -m pip install -r requirements.txt
```

Pakiety zostaną zainstalowane dokładnie w tych wersjach, które zapisaliśmy.

Warto określać wersje zależności — bez tego może się okazać, że nowa wersja jakiejś biblioteki psuje działający wcześniej projekt.

---

## Nasz pierwszy projekt w Django

Django zaopatruje nas w polecenie `django-admin`, które pozwala na tworzenie nowych projektów, appek i inne działania.

Aby stworzyć nowy projekt wykonajmy polecenie (warto zauważyć kropkę na końcu, która wskazuje na aktualny katalog):

```bash
python -m django startproject goodmovies .
```

---

## Nasz pierwszy projekt w Django

Sprawdźmy nowy projekt przy pomocy `tree`.

UNIX: `tree`, Windows: `tree /F`

Instalacja (jeśli potrzebna) na macOS:
```bash
brew install tree
```

Instalacja (jeśli potrzebna) na (Debian/Ubuntu) Linux:
```bash
sudo apt install tree
```

Następnie sprawdzamy strukturę katalogu:

```bash
tree
```

---

## Nasz pierwszy projekt w Django

* *goodmovies/* - katalog z podstawowymi ustawieniami projektu; najważniejsze pliki to `settings.py` oraz `urls.py`.

* *manage.py* - skrypt do zarządzania projektem; za chwilę zaczniemy go używać.

---

## Nasz pierwszy projekt w Django

Uruchommy więc nasz projekt poleceniem:

```bash
python manage.py runserver
```

Przejdźmy zatem do przeglądarki jak proponuje wiadomość w terminalu. Adres to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Nasz pierwszy projekt w Django

Tym samym właśnie napisaliśmy `"Hello world"` w Django! Nasza aplikacja totalnie nic nie robi, ale czy na pewno? Jeśli ujrzeliście taki widok w przeglądarce, to oznacza, że instalacja zakończyła się pomyślnie i możemy nareszcie przejść do tworzenia aplikacji.
