#!/usr/bin/python3
"""handles all CRUD RestFul API actions for places"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.review import Review


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False,
                 methods=["GET"])
def get_reviews(place_id):
    """returns all reviews in the place"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=["GET"])
def get_review(review_id):
    """returns a review"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("reviews/<review_id>",
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_review(review_id):
    """deletes a review"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("places/<place_id>/reviews",
                 strict_slashes=False,
                 methods=["POST"])
def create_review(place_id):
    """creates a review"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    payload = request.get_json()
    if "user_id" not in payload:
        abort(400, "Missing user_id")
    user = storage.get("User", payload["user_id"])
    if not user:
        abort(404)
    if "text" not in payload:
        abort(400, "Missing text")
    payload["place_id"] = place_id
    review = Review(**payload)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=["PUT"])
def update_review(review_id):
    """updates a review"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    payload = request.get_json()
    for key, value in payload.items():
        if key not in ["id", "user_id",
                       "place_id", "created_at",
                       "updated_at"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
