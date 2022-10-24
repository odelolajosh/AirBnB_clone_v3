#!/usr/bin/python3
"""handles all CRUD RestFul API actions for states"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False, methods=["GET"])
def get_states():
    """returns all states"""
    states = storage.all("State")
    states_list = [state.to_dict() for state in states.values()]
    return jsonify(states_list)


@app_views.route("/states/<state_id>",
                 strict_slashes=False,
                 methods=["GET"])
def get_state(state_id):
    """returns a state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>",
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_state(state_id):
    """deletes a state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def post_state():
    """creates a state"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    state = State(**request.get_json())
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>",
                 strict_slashes=False,
                 methods=["PUT"])
def put_state(state_id):
    """updates a state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
