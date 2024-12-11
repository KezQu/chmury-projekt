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
        self.team_name = None

    def from_form(self, form):
        self.id = 'e_' + random.randbytes(4).hex()
        self.name = form['name']
        self.surname = form['surname']
        self.experience = form['experience']
        self.contract_type = form['contract_type']
        self.hire_date = str(datetime.datetime.now())
        self.team_name = form['team_name']
        return self

    def from_record(self, record: Node):
        self.id = record.get('id')
        self.name = record.get('name')
        self.surname = record.get('surname')
        self.experience = record.get('experience')
        self.contract_type = record.get('contract_type')
        self.hire_date = record.get('hire_date')
        self.team_name = record.get('team_name')
        return self

    def __str__(self):
        return f'{self.name} {self.surname} {self.experience} {self.contract_type} {self.hire_date} {self.team_name}'

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name and self.surname == other.surname and self.experience == other.experience and self.contract_type == other.contract_type and self.hire_date == other.hire_date and self.team_name == other.team_name

    def __ne__(self, other):
        return not self == other

    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'surname': self.surname,
                'experience': self.experience,
                'contract_type': self.contract_type,
                'hire_date': self.hire_date,
                'team_name': self.team_name}

    def query_add(self):
        add_q = "CREATE (:Employee {id: $id, name: $name, surname: $surname, experience: $experience, contract_type: $contract_type, hire_date: $hire_date, team_name: $team_name})"
        return add_q, self.to_dict()


class Manager:
    def __init__(self):
        self.id = None
        self.name = None
        self.surname = None
        self.experience = None
        self.hire_date = None
        self.team_name = None

    def from_form(self, form):
        self.id = 'e_' + random.randbytes(4).hex()
        self.name = form['name']
        self.surname = form['surname']
        self.experience = form['experience']
        self.hire_date = form['hire_date']
        self.team_name = form['team_name']
        return self

    def from_record(self, record: Node):
        self.id = record.get('id')
        self.name = record.get('name')
        self.surname = record.get('surname')
        self.experience = record.get('experience')
        self.hire_date = record.get('hire_date')
        self.team_name = record.get('team_name')
        return self

    def __str__(self):
        return f'{self.name} {self.surname} {self.experience} {self.hire_date} {self.team_name}'

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name and self.surname == other.surname and self.experience == other.experience and self.hire_date == other.hire_date and self.team_name == other.team_name

    def __ne__(self, other):
        return not self == other

    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'surname': self.surname,
                'experience': self.experience,
                'hire_date': self.hire_date,
                'team_name': self.team_name}

    def query_add(self):
        add_q = "CREATE (:Manager {id: $id, name: $name, surname: $surname, experience: $experience, hire_date: $hire_date, team_name: $team_name})"
        return add_q, self.to_dict()


class Department:
    def __init__(self):
        self.id = None
        self.name = None
        self.responsibilities = None

    def from_form(self, form):
        self.id = 'e_' + random.randbytes(4).hex()
        self.name = form['name']
        self.responsibilities = form['responsibilities']
        return self

    def from_record(self, record: Node):
        self.id = record.get('id')
        self.name = record.get('name')
        self.responsibilities = record.get('responsibilities')
        return self

    def __str__(self):
        return f'{self.name} {self.responsibilities}'

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

    def from_form(self, form):
        self.id = 'e_' + random.randbytes(4).hex()
        self.name = form['name']
        self.duties = form['duties']
        return self

    def from_record(self, record: Node):
        self.id = record.get('id')
        self.name = record.get('name')
        self.duties = record.get('duties')
        return self

    def __str__(self):
        return f'{self.name} {self.duties}'

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name and self.duties == other.duties

    def __ne__(self, other):
        return not self == other

    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'duties': self.duties}

    def query_add(self):
        add_q = "CREATE (:Team {id: $id, name: $name, duties: $duties})"
        return add_q, self.to_dict()
