

from app import db

class Users(db.Model):
   
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(120), nullable=False)

    def __init__(self, name, email, password, department):
        self.name = name
        self.email = email
        self.password = password
        self.department = department


class Employees(db.Model):
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, primary_key=True)
    manager=db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(120), nullable=False)
    phone=db.Column(db.String(15), nullable=False)
    emergency_contact=db.Column(db.String(15), nullable=False)
    starting_date = db.Column(db.Date)
    status=db.Column(db.String(15), nullable=False)

    def __init__(self, name, email, manager, department, phone, emergency_contact, starting_date, status):
        self.name = name
        self.email = email
        self.manager = manager
        self.department = department
        self.phone = phone
        self.emergency_contact = emergency_contact

        self.starting_date = starting_date
        self.status = status