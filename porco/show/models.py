import json

from porco.ext import db
from porco.mixins import BasicMixin, JsonField


class LiveShow(db.Model, BasicMixin):
    id = db.Column(db.String(32), primary_key=True, index=True)

    seller_id = db.Column(db.Integer, nullable=False, index=True)
    seller_nick = db.Column(db.Unicode(32), nullable=False)

    title = db.Column(db.Unicode(128), default="")
    favor_image = db.Column(db.String(256), default="")
    cover_image = db.Column(db.String(256), default="")
    landscape = db.Column(db.Boolean, default=False)
    location = db.Column(db.Unicode(32), default="")
    approval = db.Column(db.Integer, default=0)

    # 预计开播时间
    estimated_start_at = db.Column(db.Integer, default=0)
    start_at = db.Column(db.Integer, default=0)
    end_at = db.Column(db.Integer, default=0)

    room_type = db.Column(db.Integer, default=0)
    room_status = db.Column(db.Integer, default=0)

    live_url = db.Column(db.String(512), default="")
    live_channel_id = db.Column(db.Integer, default=0)
    live_column_id = db.Column(db.Integer, default=0)

    is_free = db.Column(db.Boolean, default=False)

    # 不知道是啥
    topic = db.Column(db.String(36), default="")
    _type = db.Column(db.Integer, default=0)
    has_data_permission = db.Column(db.Boolean, default=False)
    share_to_mall = db.Column(db.String(32), default="")
    use_lcps = db.Column(db.Boolean, default=False)
    lcps_id = db.Column(db.Integer, default=0)
    feed_detail = db.Column(db.String(512), default="")
    game_id = db.Column(db.Integer, default=0)

    # 视频相关
    video_id = db.Column(db.String(32), default="")
    video_status = db.Column(db.Integer, default=0)
    video_play_url = db.Column(db.String(512), default="")
    rate_adapt = db.Column(db.Boolean, default=False)
    publish_source = db.Column(db.Integer, default=0)
    is_h265 = db.Column(db.Boolean, default=False)

    _tags, tags = JsonField("tags", lambda: [])
    _extend, extend = JsonField("extend", lambda: {})

    def update(self, data):
        self.seller_id = data["accountId"]
        self.seller_nick = data["userNick"]

        self.title = data["title"]
        self.favor_image = data["favorImg"]
        self.cover_image = data["coverImg"]
        self.landscape = data["landscape"]
        self.location = data["location"]
        self.approval = data["approval"]

        # 预计开播时间
        self.estimated_start_at = data["appointmentTime"] / 1000
        self.start_at = data["startTime"] / 1000
        self.end_at = data["endTime"] / 1000
        self.duration = data["timeLength"]

        self.room_type = data["roomType"]
        self.room_status = data["roomStatus"]

        self.live_url = data["liveUrl"]
        self.live_channel_id = data["liveChannelId"]
        self.live_column_id = data["liveColumnId"]

        # 不知道是啥
        self.is_free = data["free"]
        self.topic = data["topic"]
        self._type = data["type"]
        self.has_data_permission = data["hasDataPermission"]
        self.share_to_mall = data["share2Tmall"]
        self.use_lcps = data["useLcps"]
        self.lcps_id = data["lcpsId"]
        self.feed_detail = data["nativeFeedDetailUrl"]
        self.game_id = data["gameId"]

        video_id = data["videoId"]
        if video_id == "undefined":
            video_id = None
        self.video_id = video_id
        self.video_status = data["videoStatus"]
        self.video_play_url = data.get("videoPlayUrl")
        self.rate_adapt = data["rateAdapte"]
        self.publish_source = data["publishSource"]
        self.is_h265 = data["h265"]

        self.tags = data["tags"].split(",")
        self.extend = data["extendsMap"]

    def to_dict(self):
        return dict(
            id=self.id,
            seller=dict(id=self.seller_id, nick=self.seller_nick),
            title=self.title,
            estimated_start_at=self.estimated_start_at,
        )


class Comment(db.Model, BasicMixin):
    id = None  # hack
    show_id = db.Column(db.String(32), primary_key=True, nullable=False)
    comment_id = db.Column(db.String(32), primary_key=True, nullable=False)

    timestamp = db.Column(db.Integer, default=0)
    content = db.Column(db.UnicodeText, default="")

    from_anchor = db.Column(db.Boolean, default=False)
    private = db.Column(db.Boolean, default=False)
    reply_to_comment = db.Column(db.String(32), default="")
    reply_to_user_id = db.Column(db.String(32), default="")

    user_id = db.Column(db.String(32), index=True)
    user_nick = db.Column(db.Unicode(32), index=True)
    sns_nick = db.Column(db.Unicode(32), default="")
    taoqihi = db.Column(db.Integer, default=0)
    account_id = db.Column(db.String(32), default="")
    os = db.Column(db.String(32), default="")

    fan_score = db.Column(db.Integer, default=0)
    fan_level = db.Column(db.Integer, default=0)
    vip_user = db.Column(db.String(32))

    __table_args__ = (
        db.Index("idx_show_comment", show_id, comment_id),
    )

    def update(self, data):
        user = data["renders"]
        reply = user.get("reply")
        if reply is not None:
            reply = json.loads(reply)
        else:
            reply = {}
        device = json.loads(user["origin"].split("|")[2])

        self.timestamp = int(data["timestamp"]) / 1000
        self.content = data["content"]

        self.from_anchor = user.get("render_anchor") == "true"
        self.private = user.get("private") == "true"
        self.reply_type = reply.get("targetType")
        self.reply_to_comment = reply.get("replyToCommentId")
        self.reply_to_user_id = reply.get("replyToUserId")

        self.user_id = data["publisherId"]
        self.user_nick = data["publisherNick"]
        self.sns_nick = user.get("snsNick")

        self.taoqihi = user["taoqihi"]
        self.account_id = device["account_id"]
        self.os = device["os"]

        self.fan_score = int(user.get("fanScore", 0))
        self.fan_level = int(user.get("fanLevel", 0))
        self.vip_user = user["VIP_USER"]

    def to_dict(self):
        return dict(
            show_id=self.show_id,
            comment_id=self.comment_id,
            content=self.content,
        )