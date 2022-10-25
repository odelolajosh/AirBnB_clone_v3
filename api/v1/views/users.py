#!/usr/bin/python3
""" handles all CRUD for users """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False, methods=["GET"])
def get_users():
    """ returns all users """
    return jsonify([user.to_dict() for user in storage.all("User").values()])


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["GET"])
def get_user(user_id):
    """ returns a user """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["DELETE"])
def delete_user(user_id):
    """ delete a user by id """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def post_user():
    """ create a user """
    if not request.get_json():
        abort(400, "Not a JSON")
    for field in ["email", "password"]:
        if field not in request.get_json():
            abort(400, "Missing {}".format(field))
    user = User(**request.get_json())
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["PUT"])
def put_user(user_id):
    """ update a user """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for field in ["id", "email", "created_at", "updated_at"]:
        request.get_json().pop(field, None)
    for key, value in request.get_json().items():
        setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
