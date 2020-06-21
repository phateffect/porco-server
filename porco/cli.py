from flask_migrate import Migrate

from porco.ext import db
from porco.signals import after_boot


@after_boot.connect
def init_cmd(app):
    Migrate(app, db)