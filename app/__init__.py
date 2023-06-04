from flask import Flask
import os
from flask_mail import Mail
from config import Config
from flask_sqlalchemy import SQLAlchemy



app=Flask(__name__)
app.run(debug=True)
mail=Mail(app)

app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres@localhost:5432/postgres'
basedir=os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy(app)

