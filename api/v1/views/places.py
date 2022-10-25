#!/usr/bin/python3
""" handle CRUD for places """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False,
                 methods=["GET"])
def get_places(city_id):
    """ returns all places in the city """
    city: City = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["GET"])
def get_place(place_id):
    """ returns a place """
    place: Place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("places/<place_id>", strict_slashes=False, methods=["DELETE"])
def delete_place(place_id):
    """ deletes a place """
    place: Place = storage.get("Place", place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("cities/<city_id>/places",
                 strict_slashes=False,
                 methods=["POST"])
def create_place(city_id):
    city: City = storage.get("City", city_id)
    if not city:
        abort(404)
    if not request.json():
        abort(400, "Not a JSON")
    payload = request.json()
    if "user_id" not in payload:
        abort(400, "Missing user_id")
    user: User = storage.get("User", payload)
    if not user:
        abort(404)
    if "name" not in payload:
        abort(400, "Missing name")
    place = Place(**payload)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["PUT"])
def update_place(place_id):
    """ update a place """
    place: Place = storage.get("Place", place_id)
    if not place:
        abort(404)
    if not request.json():
        abort(400, "Not a JSON")
    for key, value in request.json().items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save(place)
    return jsonify(place.to_dict()), 200
