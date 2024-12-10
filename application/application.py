from flask import Flask, render_template
import db_driver

DB_HANDLE = db_driver.Driver()

APP = Flask(__name__)

@APP.route('/')
def index():
    return render_template('index.html')