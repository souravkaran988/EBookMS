# 📚 Kitab Ghar — EBook Management System

A full-stack web application for uploading, managing, and reading eBooks online. Users can browse books, read them directly in the browser, download PDFs, and maintain a personal reading list. Admins can approve or reject book submissions before they go live.

![Home Page](screenshots/home.png)

## 🌐 Live Demo
👉 **https://kitab-ghar-utzh.onrender.com**

> ⚠️ The app is hosted on Render's free plan. If it hasn't been visited recently, it may take **30-60 seconds to wake up** on first load. This is normal.

---

## 📌 Table of Contents
- [Features](#-features)
- [How It Works](#-how-it-works)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Run Locally](#-run-locally)
- [Environment Variables](#-environment-variables)
- [Deployment](#-deployment-on-render)
- [Known Limitations](#-known-limitations)
- [Author](#-author)

---

## ✨ Features

### 👤 User Features
- 📝 Register and log in with email and password
- 🔑 Forgot password — receive reset link via email
- 📖 Browse all approved books on the home page
- 🔍 Search books by title, author, or genre
- 👁️ View book details — description, genre, author, AI summary
- 📄 Read books directly in the browser (built-in PDF reader)
- ⬇️ Download books as properly named PDF files
- ❤️ Add or remove books from personal reading list
- 📚 View your personal library with saved books
- 🤖 Get AI-powered book recommendations based on your library

### 🛡️ Admin Features
- 🔐 Admin-only panel (role-based access control)
- ✅ Approve pending book submissions to make them live
- ❌ Reject and delete pending submissions
- 🗑️ Permanently delete any approved book
- 👁️ Preview cover image and PDF before approving

---

## 🔄 How It Works

### Book Upload Flow
1. A logged-in user fills out the upload form (title, author, genre, cover image, PDF)
2. The cover image is uploaded to **Cloudinary** (image storage)
3. The PDF is uploaded to **Cloudinary** (raw file storage)
4. Cloudinary returns permanent URLs for both files
5. Book details + Cloudinary URLs are saved to **MongoDB Atlas**
6. The book is marked as **"pending"** — not visible to other users yet
7. An Admin reviews it in the Admin Panel and **Approves** or **Rejects** it
8. Once approved, the book appears on the home page for everyone

### Reading a Book
- The PDF reader uses **Google Docs Viewer** to embed the Cloudinary PDF URL
- No local file storage is needed — everything is served from the cloud

### Downloading a Book
- Flask fetches the PDF from Cloudinary server-side
- Streams it to the user's browser as a proper `.pdf` file named after the book title

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend | Python 3, Flask | Web framework and routing |
| Database | MongoDB Atlas | Stores users and book metadata |
| File Storage | Cloudinary | Stores cover images and PDF files |
| Frontend | HTML, Jinja2, Bootstrap 4 | UI templates and styling |
| Authentication | Flask-Login, Flask-Bcrypt | Session management and password hashing |
| Forms | Flask-WTF, WTForms | Form handling and validation |
| Email | Flask-Mail, Gmail SMTP | Password reset emails |
| PDF Reader | Google Docs Viewer | Embed PDFs in browser |
| Deployment | Render | Cloud hosting |
| Version Control | Git, GitHub | Source code management |

---

## 📁 Project Structure
```
EBookMS/
│
├── app/                          # Main application package
│   ├── templates/                # All HTML templates (Jinja2)
│   │   ├── base.html             # Base layout (navbar, footer)
│   │   ├── index.html            # Home page — book listing
│   │   ├── login.html            # Login page
│   │   ├── register.html         # Registration page
│   │   ├── upload.html           # Book upload form
│   │   ├── book_details.html     # Individual book page
│   │   ├── reader.html           # In-browser PDF reader
│   │   ├── my_library.html       # User's saved books + recommendations
│   │   ├── admin_panel.html      # Admin approval dashboard
│   │   ├── reset_request.html    # Request password reset
│   │   └── reset_token.html      # Enter new password
│   │
│   ├── static/                   # Static files
│   │   ├── css/style.css         # Custom styles
│   │   ├── js/script.js          # Custom JavaScript
│   │   └── images/               # Static images (hero, logo)
│   │
│   ├── __init__.py               # App factory, config, extensions
│   ├── routes.py                 # All URL routes and view functions
│   ├── models.py                 # User class and login manager
│   ├── forms.py                  # All WTForms form classes
│   └── ai_utils.py               # Book recommendation logic
│
├── screenshots/                  # Screenshots for README
│   └── home.png
│
├── .env                          # Secret keys — NOT committed to Git
├── .gitignore                    # Files excluded from Git
├── Procfile                      # Render/Gunicorn start command
├── requirements.txt              # Python dependencies
└── run.py                        # Entry point to run the app
```

---

## 🚀 Run Locally

Follow these steps to run the project on your own machine.

### Step 1 — Clone the repository
```bash
git clone https://github.com/souravkaran988/EBookMS.git
cd EBookMS
```

### Step 2 — Create and activate virtual environment
```bash
# Create
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
```

### Step 3 — Install all dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Set up external services
You need accounts on these free services:

| Service | Purpose | Sign Up |
|---|---|---|
| MongoDB Atlas | Database | https://cloud.mongodb.com |
| Cloudinary | File storage | https://cloudinary.com |
| Gmail | Password reset emails | Use any Gmail account |

### Step 5 — Create `.env` file
Create a file named `.env` in the root folder and add:
```
SECRET_KEY=any_random_long_string_here
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?appName=Cluster0
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
MAIL_USERNAME=your_gmail@gmail.com
MAIL_PASSWORD=your_gmail_app_password
```

> 💡 For Gmail, you need to generate an **App Password** from your Google Account settings (not your regular Gmail password).

### Step 6 — Make yourself an Admin
After registering your account on the app, open Python shell:
```bash
python
```
Then run:
```python
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()
client = MongoClient(os.environ.get('MONGO_URI'))
db = client.ebook_db
db.users.update_one({"email": "your@email.com"}, {"$set": {"role": "Admin"}})
print("Done!")
exit()
```

### Step 7 — Run the app
```bash
python run.py
```
Open **http://127.0.0.1:5000** in your browser.

---

## 🔐 Environment Variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | Random string used for session security |
| `MONGO_URI` | MongoDB Atlas connection string |
| `CLOUDINARY_CLOUD_NAME` | Your Cloudinary cloud name |
| `CLOUDINARY_API_KEY` | Your Cloudinary API key |
| `CLOUDINARY_API_SECRET` | Your Cloudinary API secret |
| `MAIL_USERNAME` | Gmail address for sending reset emails |
| `MAIL_PASSWORD` | Gmail App Password (not your regular password) |

> ⚠️ Never commit your `.env` file to GitHub. It is already listed in `.gitignore`.

---

## ☁️ Deployment on Render

This app is deployed on [Render](https://render.com).

### Steps to deploy your own copy:
1. Push your code to GitHub
2. Go to https://render.com → New → Web Service
3. Connect your GitHub repository
4. Fill in these settings:

| Field | Value |
|---|---|
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn run:app` |
| Instance Type | Free |

5. Add all 7 environment variables from the table above
6. Click **Deploy**

---

## ⚠️ Known Limitations

| Limitation | Reason |
|---|---|
| Max PDF size is 10MB | Cloudinary free plan restriction |
| App sleeps after 15 min inactivity | Render free plan limitation |
| No real AI summary | Disabled to save memory on free hosting |
| No edit book feature | Not yet implemented |

---

## 📸 Screenshots

### Home Page — Book Listing
![Home Page](screenshots/home.png)

---

## 👤 Author

**Sourav Karan**
- GitHub: [@souravkaran988](https://github.com/souravkaran988)
- Live App: [kitab-ghar-utzh.onrender.com](https://kitab-ghar-utzh.onrender.com)

---

## 📄 License
This project is open source and available for learning purposes.
