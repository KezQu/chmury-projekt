from flask import Flask, render_template
import db_driver

DB_HANDLE = db_driver.Driver()

APP = Flask(__name__)

@APP.route('/')
def index():
    return render_template('index.html')

@APP.route('/lookup')
def lookup():
    return render_template('lookup.html')

@APP.route('/add_employee')
def add_employee():
    return render_template('add_employee.html')

@APP.route('/del_employee')
def del_employee():
    return render_template('del_employee.html')

@APP.route('/add_manager')
def add_manager():
    return render_template('add_manager.html')

@APP.route('/del_manager')
def del_manager():
    return render_template('del_manager.html')

@APP.route('/add_department')
def add_department():
    return render_template('add_department.html')

@APP.route('/del_department')
def del_department():
    return render_template('del_department.html')
    
@APP.route('/add_team')
def add_team():
    return render_template('add_team.html')
    
@APP.route('/del_team')
def del_team():
    return render_template('del_team.html')