from flask import Blueprint, request, jsonify
from porco.show.models import LiveShow, db

api = Blueprint("show-api", __name__)


@api.route("/shows/<show_id>", methods=["PUT"])
def update_show(show_id):
    show = LiveShow.find_or_create(id=show_id)
    show.update(request.get_json(True))
    db.session.commit()
    return jsonify(show.to_dict())