import arrow

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_admin import Admin
from porco.signals import booting


admin = Admin(name="Porco", template_mode="bootstrap3")
db = SQLAlchemy()
cors = CORS()


@booting.connect
def init_app(app):
    admin.init_app(app)
    db.init_app(app)
    cors.init_app(app)