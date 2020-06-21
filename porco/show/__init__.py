from porco.signals import booting, after_boot
from flask_admin.contrib.sqla import ModelView


@booting.connect
def init_app(app):
    from porco.show.api import api
    from porco.show import models
    app.register_blueprint(api, url_prefix="/api")


@after_boot.connect
def init_admin(app):
    from porco.ext import admin, db
    from porco.show.models import LiveShow

    admin.add_view(ModelView(LiveShow, db.session))