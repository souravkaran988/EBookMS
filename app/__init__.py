import os
from flask import Flask
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)

# 1. Security Config
# This looks for a secret key in the environment, or uses a default one for local testing
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'super_secret_key_123')

# 2. Database Config
# This looks for the MongoDB URI in the environment (Render), or uses your hardcoded one (Local)
mongo_uri = os.environ.get('MONGO_URI', "mongodb+srv://admin:password988@cluster0.xdnzcnm.mongodb.net/?appName=Cluster0")

# 3. CLOUDINARY CONFIGURATION (FOR PERMANENT FILES)
# ---------------------------------------------------------
# ⚠️ ACTION REQUIRED: REPLACE THE VALUES BELOW WITH YOUR REAL KEYS
# Get them from: https://console.cloudinary.com/console/dashboard
# ---------------------------------------------------------
cloudinary.config( 
  cloud_name = "duj6ln743", 
  api_key = "569687514872446", 
  api_secret = "WqSDBObhr12rGPCi5LqA2-HOuOk" 
)

# 4. EMAIL CONFIGURATION (Gmail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
# It looks for email/password in environment, or uses the hardcoded fallback
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'karansourav453@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'nlqz nduo zunz omra') 

# 5. Initialize Database
# We set a 5-second timeout so it doesn't hang forever if connection fails
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
# This must be at the END of the file to avoid circular import errors
from app import routes
from app import models