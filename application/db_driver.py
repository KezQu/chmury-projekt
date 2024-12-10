from neo4j import GraphDatabase as graph_db
from manager import Manager
from employee import Employee

class Driver:
    def __init__(self):
        self.URL = "neo4j://localhost:7687"
        self.CREDENTIALS = ("neo4j", "your_secure_password")

    def __del__(self):
        print('Closing connection to database')
        self.driver.close()

    def connect_to_database(self):
        self.driver = graph_db.driver(self.URL, auth=self.CREDENTIALS)
        print('Connected to', self.driver.get_server_info().agent, 'at', self.driver.get_server_info(
        ).address)

    def add_employee(self, employee: Employee):
        print("Add employee")
        pass

    def del_employee(self, employee: Employee):
        print("Del employee")
        pass

    def add_manager(self, manager: Manager):
        print("Add manager")
        pass

    def del_manager(self, manager: Manager):
        print("Del manager")
        pass

    def add_department(self, department):
        print("Add department")
        pass

    def del_department(self, department):
        print("Del department")
        pass

    def add_team(self, team):
        print("Add team")
        pass

    def del_team(self, team):
        print("Del team")
        pass