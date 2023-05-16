import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get('SECRET_KEY') or '$1$tRtdJBD.$IxanCQ7fj4Q339FQq5qr4.$1$k0Jjw//I$EfT6fv8vo5onNVHO9ecPz1'