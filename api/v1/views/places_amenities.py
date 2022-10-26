#!/usr/bin/python3
"""handles all CRUD RestFul API actions for place amenities"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place


@app_views.route("/places/<place_id>/amenities",
                 strict_slashes=False,
                 methods=["GET"])
def get_amenities(place_id):
    """returns all amenities in the place"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify([amenity.to_dict() for amenity in place.amenities])


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_amenity(place_id, amenity_id):
    """deletes an amenity"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=["POST"])
def create_amenity(place_id, amenity_id):
    """creates an amenity"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
