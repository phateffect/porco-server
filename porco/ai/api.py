from flask import Blueprint, request, jsonify
from porco.ext import smart_item

api = Blueprint("smart-api", __name__)


@api.route("/items/<int:num_iid>")
def get_smart_phrase(num_iid):
    response = smart_item.get_smart_phrase(num_iid)
    response["highlight"] = smart_item.get_highlight(response["title"])
    return jsonify(response)