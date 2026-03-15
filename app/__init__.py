import os
from flask import Flask
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import cloudinary
import cloudinary.uploader
import cloudinary.api
from dotenv import load_dotenv

# Load .env file
load_dotenv()

app = Flask(__name__)

# 1. Security Config
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# 2. Database Config
mongo_uri = os.environ.get('MONGO_URI')

# 3. Cloudinary Configuration
cloudinary.config(
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key = os.environ.get('CLOUDINARY_API_KEY'),
    api_secret = os.environ.get('CLOUDINARY_API_SECRET')
)

# 4. Email Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

# 5. Initialize Database
client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
db = client.ebook_db

# Quick connection test
try:
    client.admin.command('ping')
    print("✅ SUCCESS: Connected to MongoDB Atlas")
except Exception as e:
    print("❌ CRITICAL ERROR: Database connection failed.")
    print(e)

# 6. Initialize Plugins
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
mail = Mail(app)

# 7. Import Routes and Models
from app import routes
from app import models


