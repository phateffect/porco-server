from porco.ext import db
from porco.mixins import BasicMixin


class Comment(db.Model, BasicMixin):
    id = db.Column(db.String(64), primary=True, index=True)
    
