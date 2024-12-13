from neo4j import GraphDatabase as graph_db
from data_types import Manager, Employee, Team, Department
import os


class Driver:
    def __init__(self):
        self.URL = "neo4j+s://ca9fa5ba.databases.neo4j.io"
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

    def get_filtered_employees(self, form):
        filter = ''
        if form.get('name') is not None:
            filter += f""" e.name CONTAINS '{form.get('name')}' AND"""
        if form.get('surname') is not None:
            filter += f""" e.surname CONTAINS '{
                form.get('surname')}' AND"""
        if form.get('exp_start') is not None and not form.get('exp_start') == "":
            filter += f""" toInteger(e.experience) >= {
                form.get('exp_start')} AND"""
        if form.get('exp_end') is not None and not form.get('exp_end') == "":
            filter += f""" toInteger(e.experience) <= {
                form.get('exp_end')} AND"""
        if form.get('contract_type') is not None:
            filter += f""" e.contract_type CONTAINS '{
                form.get('contract_type')}' AND"""
        if form.get('hire_date') is not None:
            filter += f""" datetime(e.hire_date) >= datetime('{
                form.get('hire_date')}') AND"""
        filter_query_part1 = f"""MATCH (e:Employee) WHERE{filter}"""
        filter_query_part2 = f"""OPTIONAL MATCH (e:Employee)-[r:WORKS_IN]->(t:Team) WHERE{
            filter}"""
        final_query = filter_query_part1.rstrip(" WHERE").rstrip(
            "AND") + filter_query_part2.rstrip(" WHERE").rstrip(" AND") + " RETURN e, r, t"

        query_result = self.param_query(final_query, None)
        return query_result

    def get_filtered_managers(self, form):
        filter = ''
        if form.get('name') is not None:
            filter += f""" m.name CONTAINS '{form.get('name')}' AND"""
        if form.get('surname') is not None:
            filter += f""" m.surname CONTAINS '{
                form.get('surname')}' AND"""
        if form.get('exp_start') is not None and not form.get('exp_start') == "":
            filter += f""" toInteger(m.experience) >= {
                form.get('exp_start')} AND"""
        if form.get('exp_end') is not None and not form.get('exp_end') == "":
            filter += f""" toInteger(m.experience) <= {
                form.get('exp_end')} AND"""
        if form.get('hire_date') is not None:
            filter += f""" datetime(m.hire_date) >= datetime('{
                form.get('hire_date')}') AND"""
        filter_query_part1 = f"""MATCH (m:Manager) WHERE{filter}"""
        filter_query_part2 = f"""OPTIONAL MATCH (m:Manager)-[r:MANAGES]->(t:Team) WHERE{
            filter}"""
        final_query = filter_query_part1.rstrip(" WHERE").rstrip(
            "AND") + filter_query_part2.rstrip(" WHERE").rstrip(" AND") + " RETURN m, r, t"

        query_result = self.param_query(final_query, None)
        return query_result

    def get_filtered_departments(self, form):
        filter = ''
        if form.get('name') is not None:
            filter += f""" d.name CONTAINS '{form.get('name')}' AND"""
        if form.get('responsibilities') is not None:
            filter += f""" d.responsibilities CONTAINS '{
                form.get('responsibilities')}' AND"""
        filter_query_part1 = f"""MATCH (d:Department) WHERE{filter}"""
        filter_query_part2 = f"""OPTIONAL MATCH (d:Department)<-[r:IS_PART_OF]-(t:Team) WHERE{
            filter}"""
        final_query = filter_query_part1.rstrip(" WHERE").rstrip(
            "AND") + filter_query_part2.rstrip(" WHERE").rstrip(" AND") + " RETURN d, r, t"

        query_result = self.param_query(final_query, None)
        return query_result

    def get_filtered_teams(self, form):
        filter = ''
        if form.get('name') is not None:
            filter += f""" t.name CONTAINS '{form.get('name')}' AND"""
        if form.get('duties') is not None:
            filter += f""" t.duties CONTAINS '{
                form.get('duties')}' AND"""
        filter_query_part1 = f"""MATCH (t:Team) WHERE{filter}"""
        filter_query_part2 = f"""OPTIONAL MATCH (t:Team)-[r:IS_PART_OF]->(d:Department) WHERE{
            filter}"""
        final_query = filter_query_part1.rstrip(" WHERE").rstrip(
            "AND") + filter_query_part2.rstrip(" WHERE").rstrip(" AND") + " RETURN t, r, d"

        query_result = self.param_query(final_query, None)
        return query_result

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

    def get_filtered_employees_list(self, form):
        query_result = self.get_filtered_employees(form)
        print(query_result)
        return self.relations_to_list(query_result, ('e', 'r', 't'))

    def get_filtered_managers_list(self, form):
        query_result = self.get_filtered_managers(form)
        return self.relations_to_list(query_result, ('m', 'r', 't'))

    def get_filtered_departments_list(self, form):
        query_result = self.get_filtered_departments(form)
        return self.relations_to_list(query_result, ('d', 'r', 't'))

    def get_filtered_teams_list(self, form):
        query_result = self.get_filtered_teams(form)
        return self.relations_to_list(query_result, ('t', 'r', 'd'))

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
