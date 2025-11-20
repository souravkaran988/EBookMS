from pymongo import MongoClient

# Connect to Database
uri = "mongodb+srv://admin:password988@cluster0.xdnzcnm.mongodb.net/?appName=Cluster0"
client = MongoClient(uri)
db = client.ebook_db

# YOUR EMAIL IS NOW HERE
email_to_promote = "karansourav453@gmail.com"

user = db.users.find_one({"email": email_to_promote})

if user:
    db.users.update_one(
        {"_id": user["_id"]},
        {"$set": {"role": "Admin"}}
    )
    print(f"✅ Success! User {email_to_promote} is now an Admin.")
else:
    print("❌ Error: User still not found.")