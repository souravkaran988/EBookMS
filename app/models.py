from app import db, login_manager # <--- Changed mongo to db
from flask_login import UserMixin
from bson.objectid import ObjectId

@login_manager.user_loader
def load_user(user_id):
    # Changed mongo.db.users to db.users
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
        # Load the saved books (list of IDs), or empty list if none exist
        self.saved_books = user_data.get('saved_books', [])