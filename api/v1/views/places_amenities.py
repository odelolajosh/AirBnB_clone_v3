#!/usr/bin/python3
"""handles all CRUD RestFul API actions for place amenities"""

from api.v1.views import app_views
from flask import jsonify, abort
from models import storage, storage_t
from models.place import Place


@app_views.route("/places/<place_id>/amenities",
                 strict_slashes=False,
                 methods=["GET"])
def get_place_amenities(place_id):
    """returns all amenities in the place"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    if storage_t == "db":
        return jsonify([amenity.to_dict() for amenity in place.amenities])
    return jsonify([storage.get("Amenity", id).to_dict()
                    for id in place.amenity_ids])


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_place_amenity(place_id, amenity_id):
    """deletes an amenity"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    if storage_t == "db":
        if amenity not in place.amenities:
            abort(404)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=["POST"])
def create_place_amenity(place_id, amenity_id):
    """creates an amenity"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    if storage_t == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
