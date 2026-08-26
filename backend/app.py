from flask import Flask
from flask_cors import CORS

from api.routes import api


def create_app():
    app = Flask(__name__)

    # Allow requests from the React frontend
    CORS(app, resources={
        r"/api/*": {
            "origins": "http://localhost:5173"
        }
    })

    # Register API routes
    app.register_blueprint(api, url_prefix="/api")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )