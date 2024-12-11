from neo4j import GraphDatabase as graph_db
from data_types import Manager, Employee, Team, Department


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

    def delete(self, query: str, id):
        print(query)
        self.driver.execute_query(query, id=id, database_="neo4j")

    def param_query(self, query: str, params: dict):
        print(query)
        print(params)
        results, summary, keys = self.driver.execute_query(
            query, parameters_=params, database_="neo4j")
        return results

    def add_employee(self, employee: Employee):
        self.param_query(*employee.query_add())

    def add_manager(self, manager: Manager):
        self.param_query(*manager.query_add())

    def add_department(self, department: Department):
        self.param_query(*department.query_add())

    def add_team(self, team: Team):
        self.param_query(*team.query_add())

    def get_employee(self, employee_id):
        get_q = """MATCH (e:Employee {id: $id}) RETURN e"""
        return self.param_query(get_q, {'id': employee_id})

    def get_manager(self, manager_id):
        get_q = """MATCH (m:Manager {id: $id}) RETURN m"""
        return self.param_query(get_q, {'id': manager_id})

    def get_employee_all(self):
        get_all_q = """MATCH (e:Employee) RETURN e"""
        return self.param_query(get_all_q, None)

    def get_manager_all(self):
        get_all_q = """MATCH (m:Manager) RETURN m"""
        return self.param_query(get_all_q, None)

    def get_department_all(self):
        get_all_q = """MATCH (d:Department) RETURN d"""
        return self.param_query(get_all_q, None)

    def get_team_all(self):
        get_all_q = """MATCH (t:Team) RETURN t"""
        return self.param_query(get_all_q, None)

    def edit_employee(self, employee: Employee):
        print(employee)
        edit_q = """MATCH (e:Employee {id: $id}) 
                    SET e.name = $name, 
                        e.surname = $surname, 
                        e.experience = $experience, 
                        e.contract_type = $contract_type, 
                        e.team_name = $team_name"""
        return self.param_query(edit_q, employee.to_dict())

    def edit_manager(self, manager: Manager):
        edit_q = """MATCH (m:Manager {id: $id}) 
                    SET m.name = $name, 
                    m.surname = $surname, 
                    m.experience = $experience, 
                    m.team_name = $team_name"""
        return self.param_query(edit_q, manager.to_dict())

    def del_employee(self, employee_id):
        del_q = """MATCH (e:Employee {id: $id}) DETACH DELETE e"""
        self.delete(del_q, employee_id)

    def del_manager(self, manager_id):
        del_q = """MATCH (m:Manager {id: $id}) DETACH DELETE m"""
        self.delete(del_q, manager_id)

    def del_department(self, department_id, transfer_department_id):
        del_q = """MATCH (d:Department {id: $id}) DETACH DELETE d"""
        self.delete(del_q, department_id)

    def del_team(self, team_id, transfer_team_id):
        del_q = """MATCH (t:Team {id: $id}) DETACH DELETE t"""
        self.delete(del_q, team_id)
