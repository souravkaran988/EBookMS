from flask import Flask
from pymongo import MongoClient # <--- Using the standard tool, not Flask-PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

# Security Key
app.config['SECRET_KEY'] = 'super_secret_key_123'

# Database Connection (Direct)
# We use the exact method that worked in your test_db.py
try:
    uri = "mongodb+srv://admin:password988@cluster0.xdnzcnm.mongodb.net/?appName=Cluster0"
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    
    # Create the database reference directly
    # This variable 'db' will be what we import in other files
    db = client.ebook_db 
    
    # Quick check
    client.admin.command('ping')
    print("✅ SUCCESS: Connected to MongoDB Atlas (Direct Mode)")
    
except Exception as e:
    print("❌ ERROR: Could not connect to DB.")
    print(e)
    # Fallback to prevent crash, though app won't work well
    db = None

# Initialize Security
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from app import routes
from app import models