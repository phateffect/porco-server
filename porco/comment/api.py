from flask import Blueprint
from flask import request
from porco.ext import cache


api = Blueprint("comments-api", __name__)


@api.route("/comments", methods=["POST"])
def new_comments():
    data = request.get_json(True)
    seller_nick = data["seller_nick"]
    for cdata in data["comments"]:
        comment = Comment.from_data(cdata)
        if cache.has(comment.id):
            continue