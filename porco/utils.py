import time
from porco.constants import __config__


def load_config(app):
    app.config.from_pyfile(__config__)
    app.logger.warn("using local config file".center(50, "#"))


def get_ts():
    return int(time.time())