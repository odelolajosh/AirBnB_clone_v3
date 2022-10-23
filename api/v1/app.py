#!/usr/bin/python3
"""Your first endpoint (route) will be to return the status of your API:
"""

from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(error):
    """clean up method """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """404 error"""
    return jsonify(error="Not found"),  404


if __name__ == "__main__":
    PORT = getenv("HBNB_API_PORT", 5000)
    HOST = getenv("HBNB_API_HOST", "0.0.0.0")
    app.run(host=HOST, port=PORT, threaded=True)
