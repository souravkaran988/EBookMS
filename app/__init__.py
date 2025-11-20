from flask import Flask
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)

# 1. Security Config
app.config['SECRET_KEY'] = 'super_secret_key_123'

# 2. Database Config
# IMPORTANT: Check if 'password123' matches your actual MongoDB password
mongo_uri = "mongodb+srv://admin:password988@cluster0.xdnzcnm.mongodb.net/?appName=Cluster0"

# 3. EMAIL CONFIGURATION (GMAIL)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

# --- ENTER YOUR GMAIL CREDENTIALS HERE ---
app.config['MAIL_USERNAME'] = 'karansourav453@gmail.com' 
app.config['MAIL_PASSWORD'] = 'nlqz nduo zunz omra' 
# -----------------------------------------

# 4. Initialize Database (Direct Connection)
# We removed the try/except so if this fails, we know immediately.
client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
db = client.ebook_db 

# Quick Test Ping
try:
    client.admin.command('ping')
    print("✅ SUCCESS: Connected to MongoDB Atlas")
except Exception as e:
    print("❌ CRITICAL ERROR: Database connection failed.")
    print(e)

# 5. Initialize Plugins
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
mail = Mail(app)

from app import routes
from app import models