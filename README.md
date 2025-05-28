![Django Tests](https://github.com/01miru/example/actions/workflows/tests.yml/badge.svg)

WebSockety z Django
===
Przykład użycia WebSocketów w Django z wykorzystaniem biblioteki channels. W projekcie wykorzystano również bazę danych Redis jako backend do przechowywania wiadomości.
Po szerszy opis zachęcam do sprawdzenia [artykułu](https://pyjournal.pl/django-channels-i-websockety/) na moim blogu.
Podczas budowania obrazu będzie załadowana domyślna baza danych, z dwoma użytkownikami. Do logowania można użyć loginu **admin** oraz hasła **admin**.

Uruchomienie projektu
---
Aby uruchomić projekt, wykonaj następujące polecenia. Wejdź do katalogu z projektem, skopiuj przykładowy plik ustawień i uruchom kontener:

```bash
   cd example
   cp .env.example .env
   docker compose up
```

Testy
---
Korzystamu z biblioteki PyTest a całość uruchamiamy w dedykowanym kontenerze. Aby to zrobić możemy skorzystać z następującej komendy:


```bash
   docker compose -f docker-compose.yml -f docker-compose.test.yml run --rm test
```
