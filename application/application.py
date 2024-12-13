from flask import Flask, render_template, redirect, request
from data_types import Manager, Employee, Team, Department
import db_driver
from pyvis.network import Network


DB_HANDLE = db_driver.Driver()
APP = Flask(__name__)


@APP.route('/')
def index():
    manager_list = DB_HANDLE.get_manager_all_list()
    employee_list = DB_HANDLE.get_employee_all_list()
    return render_template('index.html', manager_list=manager_list, employee_list=employee_list)


@APP.route('/lookup', methods=['GET', 'POST'])
def lookup():
    nodes = []
    edges = []
    if request.method == 'GET':
        nodes, edges = DB_HANDLE.get_filtered_list(request.args)
        # nodes, edges = DB_HANDLE.get_all_list()
    graph = Network(height=600, width=800)
    for n in nodes:
        graph.add_node(n.id, label=n.name, title=str(n))
    for n1, n2, type in edges:
        graph.add_edge(n1.id, n2.id, title=type)
    graph.save_graph('./static/graph.html')
    return render_template('lookup.html')


@APP.route('/employee/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        new_employee = Employee().from_form(request.form)
        DB_HANDLE.add_employee(new_employee)
        return redirect('/')

    team_list = DB_HANDLE.get_team_all_list()
    return render_template('add_employee.html', team_list=team_list)


@APP.route('/employee/del', methods=['GET', 'POST'])
def del_employee():
    if request.method == 'POST':
        e_id = request.form['employee_id']
        DB_HANDLE.del_employee(e_id)
        return redirect('/')

    employee_list = DB_HANDLE.get_employee_all_list()
    return render_template('del_employee.html', employee_list=employee_list)


@APP.route('/employee/edit', methods=['GET', 'POST'])
def edit_employee():
    employee = None
    if request.method == 'GET':
        emp_id = request.args.get('employee_id')
        if emp_id == None:
            return redirect('/')
        employee = Employee().from_record(
            DB_HANDLE.get_employee(emp_id)[0].get('e'))

    if request.method == 'POST':
        new_employee = Employee().from_form(request.form)
        print(new_employee.to_dict())
        DB_HANDLE.edit_employee(new_employee)
        return redirect('/')

    team_list = DB_HANDLE.get_team_all_list()
    return render_template('edit_employee.html', e=employee, team_list=team_list)


@APP.route('/manager/add', methods=['GET', 'POST'])
def add_manager():
    if request.method == 'POST':
        new_manager = Manager().from_form(request.form)
        DB_HANDLE.add_manager(new_manager)
        return redirect('/')

    team_list = DB_HANDLE.get_team_all_list()
    return render_template('add_manager.html', team_list=team_list)


@APP.route('/manager/del', methods=['GET', 'POST'])
def del_manager():
    if request.method == 'POST':
        m_id = request.form['manager_id']
        DB_HANDLE.del_manager(m_id)
        return redirect('/')

    manager_list = DB_HANDLE.get_manager_all_list()
    return render_template('del_manager.html', manager_list=manager_list)


@APP.route('/manager/edit', methods=['GET', 'POST'])
def edit_manager():
    manager = None
    if request.method == 'GET':
        emp_id = request.args.get('manager_id')
        if emp_id == None:
            return redirect('/')
        manager = Manager().from_record(
            DB_HANDLE.get_manager(emp_id)[0].get('m'))

    if request.method == 'POST':
        new_manager = Manager().from_form(request.form)
        DB_HANDLE.edit_manager(new_manager)
        return redirect('/')

    team_list = DB_HANDLE.get_team_all_list()
    return render_template('edit_manager.html', m=manager, team_list=team_list)


@APP.route('/department/add', methods=['GET', 'POST'])
def add_department():
    if request.method == 'POST':
        new_dep = Department().from_form(request.form)
        DB_HANDLE.add_department(new_dep)
        return redirect('/')
    return render_template('add_department.html')


@APP.route('/department/del', methods=['GET', 'POST'])
def del_department():
    if request.method == 'POST':
        d_id = request.form['department_id']
        DB_HANDLE.del_department(d_id)
        return redirect('/')

    dep_list = DB_HANDLE.get_dep_all_list()
    return render_template('del_department.html', dep_list=dep_list)


@APP.route('/team/add', methods=['GET', 'POST'])
def add_team():
    if request.method == 'POST':
        new_team = Team().from_form(request.form)
        DB_HANDLE.add_team(new_team)
        return redirect('/')

    dep_list = DB_HANDLE.get_dep_all_list()
    return render_template('add_team.html', dep_list=dep_list)


@APP.route('/team/del', methods=['GET', 'POST'])
def del_team():
    if request.method == 'POST':
        t_id = request.form['team_id']
        DB_HANDLE.del_team(t_id)
        return redirect('/')

    team_list = DB_HANDLE.get_team_all_list()
    return render_template('del_team.html', team_list=team_list)
