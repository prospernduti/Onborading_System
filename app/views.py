from app.forms import EmployeesForm
from app import app, db
from app.models import Employees
from flask import render_template, redirect, url_for, request, flash
from flask import request,jsonify
from werkzeug.urls import url_parse
import os
import psycopg2


def db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='postgres',
                            user='postgres',
                            port="5432"
                            )
    return conn


@app.route('/update', methods=['POST'])
def update_db():
    data = request.get_json()  # Retrieve the JSON data from the request
    
    # Extract the fields from the JSON data
    name = data.get('name')
    email = data.get('email')
    department = data.get('department')

    try:
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE employees SET name = %s, email = %s, department = %s WHERE email = %s", (name, email, department, email))
        conn.commit()
        
        cur.close()
        conn.close()

        flash(f'{name} has been successfully updated!')
        return redirect(url_for('employees'))
    except psycopg2.errors.InvalidTextRepresentation as e:
        print(f"InvalidTextRepresentation: {e}")
        flash("InvalidTextRepresentation: Unable to insert into the database")
        
    except Exception as e:
        print(f"Exception: {e}")
        flash("Exception: Unable to connect to the database")


@app.route('/delete', methods=['POST'])
def delete_record():
    data = request.get_json()  # Retrieve the JSON data from the request
    
    email = data.get('email')  # Extract the email from the JSON data

    try:
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM employees WHERE email = %s", (email,))
        conn.commit()
        
        cur.close()
        conn.close()

        flash(f'Record with email {email} has been successfully deleted!')
        return 'Record deleted successfully'
    except Exception as e:
        print(f"Exception: {e}")
        flash("Exception: Unable to delete the record")
        return 'Error occurred during deletion'


@app.route('/login')
def Login():
    return render_template('login.html')
  
@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            return redirect(url_for('homepage'))
        else:
            return redirect(url_for(Login))


@app.route('/homepage')
def homepage():
    return "Hello world"

@app.route('/')
@app.route('/employees', methods=['GET', 'POST'])
def employees():
    if request.method == 'GET':
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM employees")
            rows = cur.fetchall()
            cur.close()
            conn.close()
            
            return render_template('employees.html', rows=rows)
        except Exception as e:
                print(e)
                

      
        


@app.route('/signup', methods=['POST', 'GET'])
def signup():
   
    return render_template('signup.html')

@app.route('/insert',methods=['POST', 'GET'])
def insert_db():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    department = request.form.get('department')
    try:
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO employees  VALUES (%s, %s, %s, %s)", (name, email, password, department))
        conn.commit()
        cur.close()
        conn.close()
        flash(f'{name} has been registered successfully!')
        return redirect(url_for('Login'))
    except psycopg2.errors.InvalidTextRepresentation as e:
        print(f"InvalidTextRepresentation: {e}")
        flash("InvalidTextRepresentation: Unable to insert into the database")
        return redirect(url_for('signup'))
    except Exception as e:
        print(f"Exception: {e}")
        flash("Exception: Unable to connect to the database")
        return redirect(url_for('signup'))



@app.route('/tasks')
def Onboarding_tasks():
    return render_template('onboardingTasks.html')


@app.route('/newhire')
def NewHire():
    return render_template('newHires.html')


