import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key-for-development')
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    
    # You can add database configurations and other settings here
    
    @staticmethod
    def init_app(app):
        pass 