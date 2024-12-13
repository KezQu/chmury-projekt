from neo4j import GraphDatabase as graph_db
from data_types import Manager, Employee, Team, Department
import os


class Driver:
    def __init__(self):
        self.URL = "neo4j://localhost:7687"
        with open('neo4j_auth.txt', 'r') as auth:
            credentials = auth.readline().split('/')
            self.CREDENTIALS = (credentials[0], credentials[1])

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
        print("REQUEST: ", query)
        print("REQUEST: ", params)
        results, summary, keys = self.driver.execute_query(
            query, parameters_=params, database_="neo4j")
        print("RESULT: ", results)
        return results

    def add_employee(self, employee: Employee):
        self.param_query(*employee.query_add())

    def add_manager(self, manager: Manager):
        self.param_query(*manager.query_add())

    def add_department(self, department: Department):
        self.param_query(*department.query_add())

    def add_team(self, team: Team):
        self.param_query(*team.query_add())

    def get_all(self):
        get_q = """MATCH (n1)-[r]->(n2) RETURN n1, r, n2"""
        get_orphaned_q = """MATCH (n1) WHERE NOT (n1)-[]-() RETURN n1"""
        q_result = self.param_query(get_q, None)
        q_result.extend(self.param_query(get_orphaned_q, None))
        return q_result

    def get_filtered(self, form):
        query_result = []
        query_result.extend(self.param_query(*self.search_employees(form)))
        # query_result.extend(self.param_query(self.search_managers(form)))
        # query_result.extend(self.param_query(self.search_departments(form)))
        # query_result.extend(self.param_query(self.search_teams(form)))
        return query_result

    def search_employees(self, form):
        filter = ''
        if form.get('e_name') is not None:
            filter += f""" n1.name CONTAINS '{form.get('e_name')}' AND"""
        if form.get('e_surname') is not None:
            filter += f""" n1.surname CONTAINS '{
                form.get('e_surname')}' AND"""
        if form.get('e_exp_start') is not None and not form.get('e_exp_start') == "":
            filter += f""" toInteger(n1.experience) >= {
                form.get('e_exp_start')} AND"""
        if form.get('e_exp_end') is not None and not form.get('e_exp_end') == "":
            filter += f""" toInteger(n1.experience) <= {
                form.get('e_exp_end')} AND"""
        if form.get('e_contract_type') is not None:
            filter += f""" n1.contract_type CONTAINS '{
                form.get('e_contract_type')}' AND"""
        if form.get('e_hire_date') is not None:
            filter += f""" datetime(n1.hire_date) >= datetime('{
                form.get('e_hire_date')}') AND"""
        filter_query_part1 = f"""MATCH (n1:Employee) WHERE{filter}"""
        filter_query_part2 = f"""OPTIONAL MATCH (n1:Employee)-[r:WORKS_IN]->(n2:Team) WHERE{
            filter}"""
        final_query = filter_query_part1.rstrip(" WHERE").rstrip(
            "AND") + filter_query_part2.rstrip(" WHERE").rstrip(" AND") + " RETURN n1, r, n2"

        return final_query, None

    def search_managers(self, form):
        pass

    def search_departments(self, form):
        pass

    def search_teams(self, form):
        pass

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
        return self.param_query(*employee.query_edit())

    def edit_manager(self, manager: Manager):
        return self.param_query(*manager.query_edit())

    def del_employee(self, employee_id):
        del_q = """MATCH (e:Employee {id: $id}) DETACH DELETE e"""
        self.delete(del_q, employee_id)

    def del_manager(self, manager_id):
        del_q = """MATCH (m:Manager {id: $id}) DETACH DELETE m"""
        self.delete(del_q, manager_id)

    def del_department(self, department_id):
        del_q = """MATCH (d:Department {id: $id}) DETACH DELETE d"""
        self.delete(del_q, department_id)

    def del_team(self, team_id):
        del_q = """MATCH (t:Team {id: $id}) DETACH DELETE t"""
        self.delete(del_q, team_id)

    def get_all_list(self):
        query_result = self.get_all()
        return self.relations_to_list(query_result, ('n1', 'r', 'n2'))

    def get_filtered_list(self, form):
        self.get_filtered(form)
        query_result = self.get_filtered(form)
        return self.relations_to_list(query_result, ('n1', 'r', 'n2'))

    def get_employee_all_list(self):
        query_result = self.get_employee_all()
        return self.nodes_to_list(query_result, 'e')

    def get_manager_all_list(self):
        query_result = self.get_manager_all()
        return self.nodes_to_list(query_result, 'm')

    def get_dep_all_list(self):
        query_result = self.get_department_all()
        return self.nodes_to_list(query_result, 'd')

    def get_team_all_list(self):
        query_result = self.get_team_all()
        return self.nodes_to_list(query_result, 't')

    def nodes_to_list(self, query_result, node_mark: str):
        res_list = []
        for record in query_result:
            res_list.append(self.retrieve_type_from_id(record.get(node_mark)))
        return res_list

    def relations_to_list(self, query_result, marks):
        res_list_nodes = []
        res_list_edges = []
        for record in query_result:
            obj1 = self.retrieve_type_from_id(record.get(marks[0]))
            res_list_nodes.append(obj1)
            if record.get(marks[2]) is not None:
                obj2 = self.retrieve_type_from_id(record.get(marks[2]))
                res_list_nodes.append(obj2)
            if record.get(marks[1]) is not None:
                res_list_edges.append((obj1, obj2, record.get(marks[1]).type))
        return res_list_nodes, res_list_edges

    def retrieve_type_from_id(self, record):
        if record.get('id').startswith('e_'):
            return Employee().from_record(record)
        elif record.get('id').startswith('m_'):
            return Manager().from_record(record)
        elif record.get('id').startswith('d_'):
            return Department().from_record(record)
        elif record.get('id').startswith('t_'):
            return Team().from_record(record)
