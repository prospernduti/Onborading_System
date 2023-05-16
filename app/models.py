

from app import db

class Employees(db.Model):
   
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(120), nullable=False)

    def __init__(self, name, email, password, department):
        self.name = name
        self.email = email
        self.password = password
        self.department = department
