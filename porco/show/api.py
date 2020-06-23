from flask import Blueprint, request, jsonify
from porco.ext import db
from porco.show.models import LiveShow, Comment

api = Blueprint("show-api", __name__)


@api.route("/shows/<show_id>", methods=["PUT"])
def update_show(show_id):
    show = LiveShow.find_or_create(id=show_id)
    show.update(request.get_json(True))
    db.session.commit()
    return jsonify(show.to_dict())


@api.route("/shows/<show_id>/comments", methods=["POST"])
def new_comments(show_id):
    req = request.get_json(True)
    results = []
    for data in req["comments"]:
        comment_id = data["commentId"]
        comment = Comment.find_or_create(
            show_id=show_id,
            comment_id=comment_id
        )
        comment.update(data)
        results.append(comment.to_dict())
    db.session.commit()
    return jsonify(comments=results)