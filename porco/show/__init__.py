from flask_admin.contrib.sqla import ModelView
from porco.signals import booting, after_boot
from porco.utils import format_ts

@booting.connect
def init_app(app):
    from porco.show.api import api
    from porco.show import models
    app.register_blueprint(api, url_prefix="/api")


@after_boot.connect
def live_show_admin(app):
    from porco.ext import admin, db
    from porco.show.models import LiveShow


    class LiveShowView(ModelView):
        can_edit = False
        can_view_details = True
        column_list = (
            "seller_nick",
            "start_at",
            "title",
            "tags"
        )
        column_formatters = dict(
            start_at=lambda v, c, m, p: format_ts(m.start_at),
            tags=lambda v, c, m, p: ",".join(m.tags),
        )

    admin.add_view(LiveShowView(LiveShow, db.session))

@after_boot.connect
def live_comment_admin(app):
    from porco.ext import admin, db
    from porco.show.models import Comment

    class CommentView(ModelView):
        can_edit = False
        can_view_details = True
        column_filters = (
            'show_id',
            'user_nick',
        )
        column_default_sort = [
            ("timestamp", False),
            ("show_id", True),
        ]
        column_list = (
            "show_id",
            "timestamp",
            "user_nick",
            "content",
        )
        column_formatters = dict(
            timestamp=lambda v, c, m, p: format_ts(m.timestamp),
        )

    admin.add_view(CommentView(Comment, db.session))