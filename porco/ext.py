import arrow

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_admin import Admin
from porco.signals import booting
from porco.ai.client import SmartItemClient


admin = Admin(name="Porco", template_mode="bootstrap3")
db = SQLAlchemy()
smart_item = SmartItemClient()
cors = CORS()


@booting.connect
def init_app(app):
    admin.init_app(app)
    db.init_app(app)
    cors.init_app(app)
    smart_item.init_app(app)