from flask import Flask, request, abort, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import logging


load_dotenv()
if os.getenv("LOGFILE") is not None:
    logging.basicConfig(filename='server.log', level=logging.DEBUG)

UPLOAD_DIRECTORY = f"{os.getcwd()}/{'api_uploaded_files' if os.getenv('UPLOAD_DIRECTORY') is None else os.getenv('UPLOAD_DIRECTORY')}"
ALLOWED_KEYS = os.getenv("ALLOWED_KEYS")

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

api = Flask(__name__)


@api.route("/files")
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)


@api.route("/files/<path:path>")
def get_file(path):
    """Download a file."""
    # Check if user has correct key
    user_key = request.headers.get("API-key")
    if user_key not in ALLOWED_KEYS:
        return f"Permission denied. Key '{user_key}' has no access.", 401
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


@api.route("/files", methods=["POST"])
def post_file():
    """Upload a file."""
    zipfile = request.files["zip"]
    filename = secure_filename(zipfile.filename)
    # Check if user has correct key
    user_key = request.headers.get("API-key")
    if user_key not in ALLOWED_KEYS:
        return f"Permission denied. Key '{user_key}' has no access.", 401

    if "/" in filename:
        # Return 400 BAD REQUEST
        abort(400, "no subdirectories directories allowed")

    zipfile.save(os.path.join(UPLOAD_DIRECTORY, filename))

    # Return 201 CREATED
    return "Successfully uploaded file.", 201


if __name__ == "__main__":
    api.run(debug=True, port=5000)
