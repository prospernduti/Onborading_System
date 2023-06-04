from app.forms import EmployeesForm
from app import app, db
from app.models import Employees
from flask import render_template, redirect, url_for, request
from flask import request,jsonify
from werkzeug.urls import url_parse
import datetime
import psycopg2
from app import mail
from flask_mail import Message



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
        cur.execute("UPDATE users SET name = %s, email = %s, department = %s WHERE email = %s", (name, email, department, email))
        conn.commit()
        
        cur.close()
        conn.close()

        return redirect(url_for('employees'))
    except psycopg2.errors.InvalidTextRepresentation as e:
        print(f"InvalidTextRepresentation: {e}")

        
    except Exception as e:
        print(f"Exception: {e}")



@app.route('/delete', methods=['POST'])
def delete_record():
    data = request.get_json()  # Retrieve the JSON data from the request
    
    email = data.get('email')  # Extract the email from the JSON data

    try:
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE email = %s", (email,))
        conn.commit()
        
        cur.close()
        conn.close()

        
        return 'Record deleted successfully'
    except Exception as e:
        print(f"Exception: {e}")
        
        return 'Error occurred during deletion'


@app.route('/login')
def Login():
    return render_template('login.html')
  


@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Retrieve user information from the database based on the entered username
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (username,))
        print(cur.query)  # Print the SQL query being executed

        user = cur.fetchone()
        print(user)  # Print the fetched user
        
        conn.close()
        
        if user:
            # User exists, now verify the password
            stored_password = user[2]
            stored_username=user[1]
            if stored_password == password:
                return redirect(url_for('employees'))
            elif stored_username==username:
                return "<script>alert('Unable to sign in. Please check your credentials.'); window.location.href='/login';</script>"
            
        
        # User does not exist or password is incorrect, redirect back to the login page
        else:
            return "<script>alert('Unable to sign in. Please check your credentials.'); window.location.href='/login';</script>"
            

        return redirect(url_for('Login'))


@app.route('/')
@app.route('/homepage')
def homepage():
    return render_template('index.html')


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM users")
            rows = cur.fetchall()
            cur.close()
            conn.close()
            
            return render_template('employees.html', rows=rows)
        except Exception as e:
                print(e)
                
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
            
            return render_template('employees_all.html', rows=rows)
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
        cur.execute("INSERT INTO users  VALUES (%s, %s, %s, %s)", (name, email, password, department))
        conn.commit()
        cur.close()
        conn.close()
      
        return redirect(url_for('Login'))
    except psycopg2.errors.InvalidTextRepresentation as e:
        print(f"InvalidTextRepresentation: {e}")

        return redirect(url_for('signup'))
    except Exception as e:
        print(f"Exception: {e}")
        return redirect(url_for('signup'))



@app.route('/tasks')
def Onboarding_tasks():
    return render_template('onboardingTasks.html')


@app.route('/newhire')
def NewHire():
    return render_template('newHires.html')


@app.route('/insert_new_hire',methods=['POST', 'GET'])
def insert_new_hire():
    name = request.form.get('full_name')
    starting_date=request.form.get('start_date')
    email = request.form.get('email')
    manager=request.form.get('manager')
    department = request.form.get('department')
    phone=request.form.get('phone')
    emergency_contact=request.form.get('emergency_contact_phone')
    status=request.form.get('status')
    print(f'{name}, {email}, {manager}, {department}, {phone}, {emergency_contact}, {starting_date}, {status}')
    try:
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO employees (name, email, manager, department, phone, emergency_contact, starting_date, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (name, email, manager, department, phone, emergency_contact, starting_date, status))
        conn.commit()
        cur.close()
        conn.close()
        msg=Message('Welcome to AUCA', sender=app.config['ADMINS'][0])
      
        return redirect(url_for('Onboarding_tasks'))
    except psycopg2.errors.InvalidTextRepresentation as e:
        print(f"InvalidTextRepresentation: {e}")

        return redirect(url_for('employees'))
    except Exception as e:
        print(f"Exception: {e}")
        return redirect(url_for('employees'))

@app.route('/update_emp', methods=['POST'])
def delete_emp():
    data = request.get_json()  # Retrieve the JSON data from the request
    
    name = data.get('full_name')
    starting_date=data.get('start_date')
    email = data.get('email')
    title=data.get('job_title')
    manager=data.get('manager')
    department = data.get('department')
    phone=data.get('phone')
    emergency_contact=data.get('emergency_contact_phone')
    status=data.get('status')
    
    #print(f'{name}, {email}, {manager}, {department},{title} {phone}, {emergency_contact}, {starting_date}, {status}')
    try:
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE employees SET name=%s, email=%s, manager=%s, department=%s, phone=%s, emergency_contact=%s, starting_date=%s, status=%s WHERE email = %s", (name, email, manager, department, phone, emergency_contact, starting_date, status))
        conn.commit()
        
        cur.close()
        conn.close()

        
        return 'Record has been updated successfully'
    except Exception as e:
        print(f"Exception: {e}")
        
        return 'Error occurred during updating'


@app.route('/delete_emp', methods=['POST'])
def update_emp():
    data = request.get_json()  # Retrieve the JSON data from the request
    
    # Extract the fields from the JSON data
    data = request.get_json()  # Retrieve the JSON data from the request
    
    email = data.get('email')

    try:
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM employees WHERE email = %s", (email,))
        conn.commit()
        
        cur.close()
        conn.close()

        return redirect(url_for('employees'))
    except psycopg2.errors.InvalidTextRepresentation as e:
        print(f"InvalidTextRepresentation: {e}")

        
    except Exception as e:
        print(f"Exception: {e}")