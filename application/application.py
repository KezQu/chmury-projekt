from flask import Flask, render_template, redirect, request
import db_driver
from data_types import Manager, Employee, Team, Department

DB_HANDLE = db_driver.Driver()
APP = Flask(__name__)


@APP.route('/')
def index():
    employee_query_result = DB_HANDLE.get_employee_all()
    employee_list = []
    for record in employee_query_result:
        employee_list.append(Employee().from_record(record.get('e')))
    manager_query_result = DB_HANDLE.get_manager_all()
    manager_list = []
    for record in manager_query_result:
        manager_list.append(Manager().from_record(record.get('m')))

    return render_template('index.html', manager_list=manager_list, employee_list=employee_list)


@APP.route('/lookup')
def lookup():
    return render_template('lookup.html')


@APP.route('/employee/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        new_employee = Employee().from_form(request.form)
        DB_HANDLE.add_employee(new_employee)
        return redirect('/')

    return render_template('add_employee.html')


@APP.route('/employee/del', methods=['GET', 'POST'])
def del_employee():
    if request.method == 'POST':
        e_id = request.form['employee_id']
        DB_HANDLE.del_employee(e_id)
        return redirect('/')

    return render_template('del_employee.html')


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
        DB_HANDLE.edit_employee(new_employee)
        return redirect('/')

    return render_template('edit_employee.html', e=employee)


@APP.route('/manager/add', methods=['GET', 'POST'])
def add_manager():
    if request.method == 'POST':
        new_manager = Manager().from_form(request.form)
        DB_HANDLE.add_manager(new_manager)
        return redirect('/')
    return render_template('add_manager.html')


@APP.route('/manager/del', methods=['GET', 'POST'])
def del_manager():
    if request.method == 'POST':
        m_id = request.form['manager_id']
        DB_HANDLE.del_manager(m_id)
        return redirect('/')

    return render_template('del_manager.html')


@APP.route('/manager/edit', methods=['GET', 'POST'])
def edit_manager():
    manager = None
    if request.method == 'GET':
        man_id = request.form.get('manager_id')
        if man_id == None:
            return redirect('/')
        manager = DB_HANDLE.get_manager(man_id)

    if request.method == 'POST':
        new_manager = Manager().from_form(request.form)
        DB_HANDLE.edit_manager(new_manager)
        return redirect('/')

    return render_template('edit_manager.html')


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
        transter_d_id = request.form['transfer_department_id']
        DB_HANDLE.del_department(d_id, transter_d_id)
        return redirect('/')

    return render_template('del_department.html')


@APP.route('/team/add', methods=['GET', 'POST'])
def add_team():
    if request.method == 'POST':
        new_team = Team().from_form(request.form)
        DB_HANDLE.add_team(new_team)
        return redirect('/')
    return render_template('add_team.html')


@APP.route('/team/del', methods=['GET', 'POST'])
def del_team():
    if request.method == 'POST':
        t_id = request.form['team_id']
        transter_t_id = request.form['transfer_team_id']
        DB_HANDLE.del_team(t_id, transter_t_id)
        return redirect('/')

    return render_template('del_team.html')
