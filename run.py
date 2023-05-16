from app import app,db

from app import views
from app.models import Employees

app.app_context().push()
db.create_all()