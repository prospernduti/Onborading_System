from app import app,db

from app import views
from app.models import Employees,Users

app.app_context().push()
db.create_all()