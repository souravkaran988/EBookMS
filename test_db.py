from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# PASTE YOUR CONNECTION STRING HERE (The one from config.py)
# It should look like: "mongodb+srv://admin:password123@cluster0....."
uri = "mongodb+srv://admin:password988@cluster0.xdnzcnm.mongodb.net/?appName=Cluster0"

print("-----------------------------------------")
print("Attempting to connect to MongoDB Atlas...")
print("-----------------------------------------")

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000) # 5 second timeout
    # This command forces a connection to check if it works
    client.admin.command('ping')
    print("✅ SUCCESS! Connected to MongoDB Atlas.")
    print("The connection string is correct.")
except ConnectionFailure:
    print("❌ ERROR: Could not connect to MongoDB Atlas.")
    print("Possible causes:")
    print("1. IP Address not whitelisted (Network Access in Atlas).")
    print("2. Wrong Password.")
    print("3. Firewall blocking the connection.")
except Exception as e:
    print(f"❌ An unexpected error occurred: {e}")

print("-----------------------------------------")