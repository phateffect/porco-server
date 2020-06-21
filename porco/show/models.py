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
        self.estimated_start_at = data["appointmentTime"]
        self.start_at = data["startTime"]
        self.end_at = data["endTime"]
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

        self.video_id = data["videoId"]
        self.video_status = data["videoStatus"]
        self.video_play_url = data["videoPlayUrl"]
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