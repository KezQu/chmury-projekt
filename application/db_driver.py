from neo4j import GraphDatabase as graph_db


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

    def add_employee(self):
        print("Add employee")
        pass

    def del_employee(self):
        print("Del employee")
        pass

    def add_manager(self):
        print("Add manager")
        pass

    def del_manager(self):
        print("Del manager")
        pass

    def add_department(self):
        print("Add department")
        pass

    def del_department(self):
        print("Del department")
        pass
