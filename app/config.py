import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'devices.db')
SECRET_KEY = 'secret_key'
CELERY_BROKER_URL = 'amqp://localhost//'
CELERY_BACKEND = 'amqp'
#DEBUG = False
