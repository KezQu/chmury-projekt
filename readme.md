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

## Diagram klas

```plantuml

package "Database Types"{
class Employee{
  + id
  + name
  + surname
  + experience
  + contract_type
  + hire_date
  + works_in
  __
  + from_form()
  + from_record()
  + to_dict()
  + query_add()
  + query_edit()
}

class Manager{
  + id
  + name
  + surname
  + experience
  + hire_date
  + works_in
  __
  + from_form()
  + from_record()
  + to_dict()
  + query_add()
  + query_edit()

}
class Department{}
class Team{}

}
class Driver{
  + connect_to_database()
  + delete()
  + param_query()
  + add_employee()
  + add_manager()
  + add_department()
  + add_team()
  + get_all()
  + get_filtered_employees()
  + get_filtered_managers()
  + get_filtered_departments()
  + get_filtered_teams()
  + get_employee()
  + get_manager()
  + get_employee_all()
  + get_manager_all()
  + get_department_all()
  + get_team_all()
  + edit_employee()
  + edit_manager()
  + del_employee()
  + del_manager()
  + del_department()
  + del_team()
  + get_all_list()
  + get_employee_all_list()
  + get_manager_all_list()
  + get_dep_all_list()
  + get_team_all_list()
  + get_filtered_employees_list()
  + get_filtered_managers_list()
  + get_filtered_departments_list()
  + get_filtered_teams_list()
  + nodes_to_list()
  + relations_to_list()
  + retrieve_type_from_id()
}

```
