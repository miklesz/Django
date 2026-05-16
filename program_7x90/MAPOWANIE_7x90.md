# Mapowanie materialu: oryginal -> 7 cwiczen

## Podstawa podzialu
- Zrodlo: oryginalne notebooki `1..8` oraz `6a` (bez `0_Run.ipynb`).
- Suma materialu: `650` komorek.
- Cel orientacyjny: ok. `93` komorki na cwiczenie (`650/7 = 92.86`).
- Ciecia tylko na granicach pod-tematow (naglowki), bez rozbijania srodka sekcji.

## Nowe cwiczenia i zakresy
| Cwiczenie | Nowy plik | Zakres zrodlowy | Liczba komorek |
|---|---|---|---:|
| 1 | `1_Fundamenty_i_start_aplikacji.ipynb` | `1:0..87`, `2:0..1` → bez URL Resolver, +IDE | 96 |
| 2 | `2_Widoki_migracje_admin_i_kontekst.ipynb` | URL Resolver (z 01) + `2:2..84` | 92 |
| 3 | `3_Model_danych_i_wejscie_w_szablony.ipynb` | Kontekst (z 02) + `2:103..108`, `3:0..53`, `4:0..27` | 106 |
| 4 | `4_Prezentacja_danych_i_relacje_modeli.ipynb` | `4:28..54`, `5:0..66` | 94 |
| 5 | `5_Rozbudowa_modelu_i_widoki_klasowe.ipynb` | `5:67..71`, `6:0..57`, `6a:0..27` | 91 |
| 6 | `6_Linkowanie_i_autoryzacja_podstawy.ipynb` | `6a:28..38`, `7:0..69`, `8:0..10` | 92 |
| 7 | `7_Rejestracja_i_rozszerzenia_interfejsu.ipynb` | `8:11..104` | 94 |

## Rozklad wielkosci
- 1: 102  (+12 vs cel 90) ✅
- 2: 92   (+2 vs cel 90) ✅
- 3: 106  (+16 vs cel 90, edycja zaplanowana razem z 4) ✅
- 4: 94   (+4 vs cel 90) ✅
- 5: 91   (+1 vs cel 90) ✅
- 6: 92   (+2 vs cel 90) ✅
- 7: 94   (+4 vs cel 90) ✅
- **Razem: 671 minut (~11 godzin 11 minut)**
- **Średnio: 95 minut na lekcję**

Wszystkie lekcje są w tolerancji ±15 minut od celu 90 minut ✅

## Uwagi
- Wygładzenie `2`/`3` wykonane bez zmiany kolejnosci merytorycznej, przez nowy punkt ciecia na granicy naglowkow.
- Rozklad jest bardziej rowny niz poprzednio, bez ciecia srodka pod-tematu.
- 2026-05-14: dodano sekcje IDE do `1` (+15 komorek).
- 2026-05-14: URL Resolver (9 komorek) przesuniety z konca `1` do poczatku `2`; Kontekst w szablonach HTML (18 komorek) przesuniety z konca `2` do poczatku `3`. Cel: `1` i `2` w tolerancji +/-15 min.
