from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from tasks_celery import make_celery


app = Flask(__name__)
app.config.from_pyfile('config.py')
Bootstrap(app)
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
admin = Admin(app)
celery = make_celery(app)

#celery = Celery(app.name, backend=app.config['CELERY_RESULT_BACKEND'], broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)

from views import *
from views_results import *
from api_restful import *
from models import *


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=12346, use_reloader=True, threaded=True)
