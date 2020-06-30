from flask import Flask

from porco.signals import booting, after_boot
from porco.utils import load_config
from porco import ai # NOQA
from porco import cli  # NOQA
from porco import ext  # NOQA
from porco import show  # NOQA

app = Flask(__name__)
load_config(app)

booting.send(app)
after_boot.send(app)