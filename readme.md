# Struktura organizacyjna firmy

## Pierwsze uruchomienie

W celu uruchomienia aplikacji wraz z bazą danych należy stworzyć plik `neo4j_auth.txt`
zawierający nazwę użytkownika oraz hasło służące do zalogowania do bazy danych.

Przykładowa zawartość pliku `nazwa/hasło`.

Po utworzeniu pliku konfiguracyjnego dane użytkownika z folderu głównego projektu
należy uruchomić komendę `docker compose up -d` w celu zbudowania bazy danych
wraz z aplikacją użytkownika. Po skonfigurowaniu kontenerów pod adresem
`127.0.0.1:2137` zostanie uruchomiona aplikacja użytkownika.

## Kolejne uruchomienia

Aby ponownie uruchomić aplikację zawartość pliku `neo4j_auth.txt` musi być identyczna
jak w przypadku pierwszego uruchomienia, następnie w celu uruchomienia aplikacji należy
użyć komendy `docker compose up -d`.
