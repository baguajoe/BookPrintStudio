import os
from flask import Flask, jsonify, send_from_directory
from flask_migrate import Migrate
from flask_cors import CORS
from api.utils import APIException, generate_sitemap
from api.models import db
from api.routes import api, pricing_api  # Import the blueprints
from api.admin import setup_admin
from api.commands import setup_commands

# App setup
app = Flask(__name__)
app.url_map.strict_slashes = False

# Enable CORS
CORS(app)

# Environment-based settings
ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../public/")

# Database configuration
db_url = os.getenv("DATABASE_URL")
if db_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url.replace(
        "postgres://", "postgresql://"
    )  # Fix for psycopg2
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tmp/test.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database and migration tools
db.init_app(app)
MIGRATE = Migrate(app, db, compare_type=True)

# Register blueprints
app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(pricing_api, url_prefix="/pricing")

# Setup admin panel and CLI commands
setup_admin(app)
setup_commands(app)

# Error handling
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Sitemap generation for development
@app.route("/")
def sitemap():
    if ENV == "development":
        return generate_sitemap(app)
    return send_from_directory(static_file_dir, "index.html")

# Static file serving for production
@app.route("/<path:path>", methods=["GET"])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = "index.html"
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0  # Avoid cache memory
    return response

# Entry point
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3001))
    app.run(host="0.0.0.0", port=PORT, debug=True)
