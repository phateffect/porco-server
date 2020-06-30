from porco.signals import booting

@booting.connect
def init_app(app):
    from porco.ai.api import api
    app.register_blueprint(api, url_prefix="/ai")