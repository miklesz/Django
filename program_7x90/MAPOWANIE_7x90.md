# Mapowanie materialu: oryginal -> 7 cwiczen

## Podstawa podzialu
- Zrodlo: oryginalne notebooki `1..8` oraz `6a` (bez `0_Run.ipynb`).
- Suma materialu: `650` komorek.
- Cel orientacyjny: ok. `93` komorki na cwiczenie (`650/7 = 92.86`).
- Ciecia tylko na granicach pod-tematow (naglowki), bez rozbijania srodka sekcji.

## Nowe cwiczenia i zakresy
| Cwiczenie | Nowy plik | Zakres zrodlowy | Liczba komorek |
|---|---|---|---:|
| 01 | `01_Fundamenty_i_start_aplikacji.ipynb` | `1:0..87`, `2:0..1` → bez URL Resolver, +IDE | 96 |
| 02 | `02_Widoki_migracje_admin_i_kontekst.ipynb` | URL Resolver (z 01) + `2:2..84` | 92 |
| 03 | `03_Model_danych_i_wejscie_w_szablony.ipynb` | Kontekst (z 02) + `2:103..108`, `3:0..53`, `4:0..27` | 106 |
| 04 | `04_Prezentacja_danych_i_relacje_modeli.ipynb` | `4:28..54`, `5:0..66` | 94 |
| 05 | `05_Rozbudowa_modelu_i_widoki_klasowe.ipynb` | `5:67..71`, `6:0..57`, `6a:0..27` | 91 |
| 06 | `06_Linkowanie_i_autoryzacja_podstawy.ipynb` | `6a:28..38`, `7:0..69`, `8:0..10` | 92 |
| 07 | `07_Rejestracja_i_rozszerzenia_interfejsu.ipynb` | `8:11..104` | 94 |

## Rozklad wielkosci
- 01: 96  (+6 vs cel 90)
- 02: 92  (+2 vs cel 90)
- 03: 106 (+16 vs cel 90, edycja zaplanowana razem z 04)
- 04: 94
- 05: 91
- 06: 92
- 07: 94

## Uwagi
- Wygładzenie `02`/`03` wykonane bez zmiany kolejnosci merytorycznej, przez nowy punkt ciecia na granicy naglowkow.
- Rozklad jest bardziej rowny niz poprzednio, bez ciecia srodka pod-tematu.
- 2026-05-14: dodano sekcje IDE do `01` (+15 komorek).
- 2026-05-14: URL Resolver (9 komorek) przesuniety z konca `01` do poczatku `02`; Kontekst w szablonach HTML (18 komorek) przesuniety z konca `02` do poczatku `03`. Cel: `01` i `02` w tolerancji +/-15 min.
