#!/usr/bin/python3
""" handles all CRUD for amenities """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False, methods=["GET"])
def get_amenities():
    """ returns all amenities """
    return jsonify([
        amenity.to_dict()
        for amenity in storage.all("Amenity").values()])


@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=["GET"])
def get_amenity(amenity_id):
    """ returns an amenity """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_amenity(amenity_id):
    """ delete an amenity by id """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def post_amenity():
    """ create an amenity """
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    amenity = Amenity(**request.get_json())
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=["PUT"])
def put_amenity(amenity_id):
    """ update an amenity """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
