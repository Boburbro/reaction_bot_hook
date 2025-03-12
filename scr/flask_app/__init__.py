from flask import Flask

def create_app():
    app = Flask(__name__)

    from .routes.index import index
    from .routes.bots import bots
    from .routes.create_data_base import create_data_base

    app.register_blueprint(index, url_prefix="/")
    app.register_blueprint(bots, url_prefix="/bots")
    app.register_blueprint(create_data_base, url_prefix="/create-data-base")

    return app
