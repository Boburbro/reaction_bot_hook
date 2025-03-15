from flask import Flask
from flask_login import LoginManager
from .config import Config
from .models import User

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    # In a real application, you would query a database
    # For this example, we'll use a hardcoded admin user
    if int(user_id) == 1:
        return User(1, 'admin', 'password_hash')
    return None

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.url_map.strict_slashes = False
    
    login_manager.init_app(app)
    
    from .routes.index import index
    from .routes.bots import bots
    from .routes.create_data_base import create_data_base
    from .routes.auth import auth

    app.register_blueprint(index, url_prefix="/")
    app.register_blueprint(bots, url_prefix="/bots")
    app.register_blueprint(create_data_base, url_prefix="/create-data-base")
    app.register_blueprint(auth, url_prefix="/auth")

    return app
