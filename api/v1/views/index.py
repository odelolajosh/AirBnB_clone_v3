#!/usr/bin/python3
""" create route for blueprint that returns a json """

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", strict_slashes=False)
def status():
    """return json status"""
    return jsonify({"status": "OK"})
