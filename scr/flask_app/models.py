from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_authenticated(self):
        return True
        
    @property
    def is_anonymous(self):
        return False
        
    def get_id(self):
        return str(self.id)
        
    @staticmethod
    def get_user(username):
        # In a real application, you would query a database
        # For this example, we'll use a hardcoded admin user
        if username == 'admin':
            return User(1, 'admin', generate_password_hash('1234'))
        return None
    
    @staticmethod
    def verify_password(user, password):
        if user is None:
            return False
        return check_password_hash(user.password_hash, password) 