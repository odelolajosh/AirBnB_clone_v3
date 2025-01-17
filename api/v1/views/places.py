#!/usr/bin/python3
"""handles all CRUD RestFul API actions for places"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False,
                 methods=["GET"])
def get_places(city_id):
    """returns all places in the city"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["GET"])
def get_place(place_id):
    """returns a place"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("places/<place_id>", strict_slashes=False, methods=["DELETE"])
def delete_place(place_id):
    """deletes a place"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("cities/<city_id>/places",
                 strict_slashes=False,
                 methods=["POST"])
def create_place(city_id):
    """creates a place"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    payload = request.get_json()
    if "user_id" not in payload:
        abort(400, "Missing user_id")
    user = storage.get("User", payload["user_id"])
    if not user:
        abort(404)
    if "name" not in payload:
        abort(400, "Missing name")
    payload["city_id"] = city_id
    place = Place(**payload)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["PUT"])
def update_place(place_id):
    """update a place"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
