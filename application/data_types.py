import random
from neo4j.graph import Node
import datetime


class Employee:
    def __init__(self):
        self.id = None
        self.name = None
        self.surname = None
        self.experience = None
        self.contract_type = None
        self.hire_date = None
        self.works_in = None

    def from_form(self, form):
        if form.get('id') is None:
            self.id = 'e_' + random.randbytes(4).hex()
        else:
            self.id = form['id']
        self.name = form['name']
        self.surname = form['surname']
        self.experience = form['experience']
        self.contract_type = form['contract_type']
        if form.get('hire_date') is None:
            self.hire_date = str(datetime.datetime.now())
        else:
            self.hire_date = form['hire_date']
        if form.get('works_in') is not None:
            self.works_in = form['works_in']

        return self

    def from_record(self, record: Node):
        self.id = record.get('id')
        self.name = record.get('name')
        self.surname = record.get('surname')
        self.experience = record.get('experience')
        self.contract_type = record.get('contract_type')
        self.hire_date = record.get('hire_date')
        return self

    def __str__(self):
        return f'{self.name}\n{self.surname}\n{self.experience}\n{self.contract_type}\n{self.hire_date}'

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name and self.surname == other.surname and self.experience == other.experience and self.contract_type == other.contract_type and self.hire_date == other.hire_date

    def __ne__(self, other):
        return not self == other

    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'surname': self.surname,
                'experience': self.experience,
                'contract_type': self.contract_type,
                'hire_date': self.hire_date,
                'works_in': self.works_in}

    def query_add(self):
        add_q = "CREATE (:Employee {id: $id, name: $name, surname: $surname, experience: $experience, contract_type: $contract_type, hire_date: $hire_date})"
        if self.works_in is not None:
            add_q = add_q + \
                " WITH $id AS emp_id MATCH (e:Employee {id: emp_id}) MATCH (t:Team {id: $works_in}) CREATE (e)-[:WORKS_IN]->(t)"
        return add_q, self.to_dict()

    def query_edit(self):
        edit_q = """MATCH (e:Employee {id: $id})
                    SET e.name = $name,
                        e.surname = $surname,
                        e.experience = $experience,
                        e.contract_type = $contract_type"""
        if self.works_in is not None:
            edge_edit_q = ''
            if self.works_in == 'Delete':
                edge_edit_q = " WITH $id AS emp_id MATCH (e:Employee {id: emp_id})-[r:WORKS_IN]->() DELETE r"
            else:
                edge_edit_q = " WITH $id AS emp_id MATCH (e:Employee {id: emp_id}) MATCH (t:Team {id: $works_in}) CREATE (e)-[:WORKS_IN]->(t)"
            edit_q = edit_q + edge_edit_q
        return edit_q + " RETURN e", self.to_dict()


class Manager:
    def __init__(self):
        self.id = None
        self.name = None
        self.surname = None
        self.experience = None
        self.hire_date = None
        self.manages = None

    def from_form(self, form):
        if form.get('id') is None:
            self.id = 'm_' + random.randbytes(4).hex()
        else:
            self.id = form['id']
        self.name = form['name']
        self.surname = form['surname']
        self.experience = form['experience']
        if form.get('hire_date') is None:
            self.hire_date = str(datetime.datetime.now())
        else:
            self.hire_date = form['hire_date']
        if form.get('manages') is not None:
            self.manages = form['manages']
        return self

    def from_record(self, record: Node):
        self.id = record.get('id')
        self.name = record.get('name')
        self.surname = record.get('surname')
        self.experience = record.get('experience')
        self.hire_date = record.get('hire_date')
        return self

    def __str__(self):
        return f'{self.name}\n{self.surname}\n{self.experience}\n{self.hire_date}'

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name and self.surname == other.surname and self.experience == other.experience and self.hire_date == other.hire_date

    def __ne__(self, other):
        return not self == other

    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'surname': self.surname,
                'experience': self.experience,
                'hire_date': self.hire_date,
                'manages': self.manages}

    def query_add(self):
        add_q = "CREATE (:Manager {id: $id, name: $name, surname: $surname, experience: $experience, hire_date: $hire_date})"
        if self.manages is not None:
            add_q = add_q + \
                " WITH $id AS man_id MATCH (m:Manager {id: man_id}) MATCH (t:Team {id: $manages}) CREATE (m)-[:MANAGES]->(t)"
        return add_q, self.to_dict()

    def query_edit(self):
        edit_q = """MATCH (m:Manager {id: $id})
                    SET m.name = $name,
                    m.surname = $surname,
                    m.experience = $experience"""
        if self.manages is not None:
            edit_q = edit_q + \
                " WITH $id AS man_id MATCH (m:Manager {id: man_id}) MATCH (t:Team {id: $manages}) CREATE (m)-[:MANAGES]->(t)"
        return edit_q + " RETURN m", self.to_dict()


class Department:
    def __init__(self):
        self.id = None
        self.name = None
        self.responsibilities = None

    def from_form(self, form):
        if form.get('id') is None:
            self.id = 'd_' + random.randbytes(4).hex()
        else:
            self.id = form['id']
        self.name = form['name']
        self.responsibilities = form['responsibilities']
        return self

    def from_record(self, record: Node):
        self.id = record.get('id')
        self.name = record.get('name')
        self.responsibilities = record.get('responsibilities')
        return self

    def __str__(self):
        return f'{self.name}\n{self.responsibilities}'

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name and self.responsibilities == other.responsibilities

    def __ne__(self, other):
        return not self == other

    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'responsibilities': self.responsibilities}

    def query_add(self):
        add_q = "CREATE (:Department {id: $id, name: $name, responsibilities: $responsibilities})"
        return add_q, self.to_dict()


class Team:
    def __init__(self):
        self.id = None
        self.name = None
        self.duties = None
        self.is_part_of = None

    def from_form(self, form):
        if form.get('id') is None:
            self.id = 't_' + random.randbytes(4).hex()
        else:
            self.id = form['id']
        self.name = form['name']
        self.duties = form['duties']
        if form.get('is_part_of') is not None:
            self.is_part_of = form['is_part_of']

        return self

    def from_record(self, record: Node):
        self.id = record.get('id')
        self.name = record.get('name')
        self.duties = record.get('duties')
        return self

    def __str__(self):
        return f'{self.name}\n{self.duties}'

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name and self.duties == other.duties

    def __ne__(self, other):
        return not self == other

    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'duties': self.duties,
                'is_part_of': self.is_part_of}

    def query_add(self):
        add_q = "CREATE (:Team {id: $id, name: $name, duties: $duties})"
        if self.is_part_of is not None:
            add_q = add_q + \
                " WITH $id AS team_id MATCH (t:Team {id: team_id}) MATCH (d:Department {id: $is_part_of}) CREATE (t)-[:IS_PART_OF]->(d)"

        return add_q, self.to_dict()
