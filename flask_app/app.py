import logging

from flask import Flask

from views import bp as routes_bp

logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    app.register_blueprint(routes_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
