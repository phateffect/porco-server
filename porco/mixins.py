import json

from wtforms.fields import Field, SelectField
from wtforms.widgets import TextArea

from porco.ext import db
from porco.utils import get_ts


class BasicMixin(object):
    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.Integer, default=get_ts, nullable=False)
    updated_at = db.Column(
        db.Integer,
        default=get_ts,
        onupdate=get_ts,
        nullable=False,
    )

    @classmethod
    def find_or_create(cls, **kwargs):
        if kwargs:
            item = cls.query.filter_by(**kwargs).first()
            if item is None:
                item = cls(**kwargs)
                db.session.add(item)
            return item
        raise ValueError("parameter is empty!")


def JsonField(name, default_fn):  # NOQA: N802
    field = db.Column(name, db.Text(16777215))  # MText
    fname = "_{0}".format(name)

    def getter(instance):
        attr = getattr(instance, fname)
        if attr:
            return json.loads(attr)
        return default_fn()

    def setter(instance, new_val):
        setattr(instance, fname, json.dumps(new_val))
        return new_val

    return field, property(getter, setter)


def EnumField(name, default, nullable=True):  # NOQA: N802
    enum_cls = default.__class__
    field = db.Column(name, db.Integer, index=True, default=default.value)
    fname = "_{0}".format(name)

    def getter(instance):
        attr = getattr(instance, fname)
        return enum_cls(attr)

    def setter(instance, value):
        if isinstance(value, str):
            value = enum_cls[value]
        else:
            value = enum_cls(value)
        setattr(instance, fname, value.value)
        return value

    def expression(cls):
        return getattr(cls, fname)

    return field, hybrid_property(getter, setter, expression)


class FormJsonField(Field):
    widget = TextArea()

    def _value(self):
        if self.data:
            return json.dumps(self.data, indent=4, ensure_ascii=False)
        return "{\n    \n}"

    def process_formdata(self, value):
        self.data = json.loads(value[0])


class FormEnumField(SelectField):
    def __init__(self, enum_class, label, *args, **kwargs):
        self.enum_class = enum_class
        choices = [
            (value.name, value.name)
            for __, value in enum_class.__members__.items()
        ]
        super(FormEnumField, self).__init__(
            label, choices=choices,
            *args, **kwargs
        )

    def process_data(self, value):
        if value:
            self.data = value.name
        else:
            self.data = self.enum_class(0).name

    def process_formdata(self, values):
        self.data = self.enum_class[values[0]].name