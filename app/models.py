from app import db, login_manager, app
from flask_login import UserMixin
from bson.objectid import ObjectId
from itsdangerous import URLSafeTimedSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    user_data = db.users.find_one({"_id": ObjectId(user_id)})
    if not user_data:
        return None
    return User(user_data)

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data.get('username')
        self.email = user_data.get('email')
        self.role = user_data.get('role', 'User')
        self.saved_books = user_data.get('saved_books', [])

    # Generate a secure token for password reset
    def get_reset_token(self):
        # Creates a token that expires in 30 minutes (1800 seconds)
        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id}, salt='password-reset-salt')

    # Verify the token
    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, salt='password-reset-salt', max_age=expires_sec)['user_id']
        except:
            return None
        
        # Find the user in the database
        user_data = db.users.find_one({"_id": ObjectId(user_id)})
        if not user_data:
            return None
        return User(user_data)