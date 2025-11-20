import os
import secrets
from flask import render_template, url_for, flash, redirect, request, current_app
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, BookForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from bson.objectid import ObjectId
import PyPDF2

# Import AI functions
from app.ai_utils import generate_summary, get_recommendations

# --- 1. GATEKEEPER ROUTE ---
@app.route("/")
def root():
    # If user is logged in, send them to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # If not, force them to the Login page immediately
    return redirect(url_for('login'))

# --- 2. DASHBOARD & SEARCH ---
@app.route("/home")
@login_required
def home():
    # Get the search query from the URL (e.g., /home?q=python)
    query = request.args.get('q')
    
    if query:
        # Search for books where Title OR Genre OR Author contains the query
        books = list(db.books.find({
            "status": "approved",
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"genre": {"$regex": query, "$options": "i"}},
                {"author": {"$regex": query, "$options": "i"}}
            ]
        }))
    else:
        # Show all approved books (Newest first)
        books = list(db.books.find({"status": "approved"}).sort("_id", -1))
        
    return render_template('index.html', books=books)

# --- 3. AUTHENTICATION ROUTES ---
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_data = {
            "username": form.username.data,
            "email": form.email.data,
            "password": hashed_password,
            "role": "User", # Default role
            "saved_books": [] # Initialize empty reading list
        }
        db.users.insert_one(user_data)
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user_data = db.users.find_one({"email": form.email.data})
        if user_data and bcrypt.check_password_hash(user_data['password'], form.password.data):
            user_obj = User(user_data)
            login_user(user_obj, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login')) # Redirect to login page after logout

# --- 4. HELPER FUNCTION FOR FILES ---
def save_file(form_file, folder_name):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_file.filename)
    filename = random_hex + f_ext
    file_path = os.path.join(app.root_path, 'static', folder_name, filename)
    form_file.save(file_path)
    return filename, file_path

# --- 5. UPLOAD BOOK ROUTE ---
@app.route("/book/new", methods=['GET', 'POST'])
@login_required
def new_book():
    form = BookForm()
    if form.validate_on_submit():
        if form.pdf.data and form.cover_photo.data:
            # Save Files
            pdf_filename, pdf_path = save_file(form.pdf.data, 'uploads')
            cover_filename, _ = save_file(form.cover_photo.data, 'covers')
            
            # Determine Genre (Dropdown vs Custom)
            final_genre = form.custom_genre.data if form.genre.data == 'Other' else form.genre.data
            
            # Extract Text for AI
            text_content = ""
            try:
                with open(pdf_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    # Extract first 10 pages only for speed
                    for page in reader.pages[:10]: 
                        text_content += page.extract_text()
            except Exception as e:
                print(f"Error reading PDF: {e}")
                text_content = "Could not read text from PDF."

            # Save to DB
            book_data = {
                "title": form.title.data,
                "author": form.author.data,
                "genre": final_genre,
                "description": form.description.data,
                "cover_image": cover_filename,
                "pdf_file": pdf_filename,
                "content": text_content,
                "user_id": current_user.id,
                "status": "pending", # Pending Admin Approval
                "summary": "No summary yet"
            }
            db.books.insert_one(book_data)
            flash('Book uploaded successfully! It is pending approval.', 'success')
            return redirect(url_for('home'))
            
    return render_template('upload.html', title='New Book', form=form)

# --- 6. BOOK DETAILS & READER ---
@app.route("/book/<book_id>")
def book_details(book_id):
    book = db.books.find_one({"_id": ObjectId(book_id)})
    if not book:
        flash('Book not found!', 'warning')
        return redirect(url_for('home'))
    return render_template('book_details.html', title=book.get('title'), book=book)

@app.route("/book/<book_id>/read")
@login_required
def read_book(book_id):
    book = db.books.find_one({"_id": ObjectId(book_id)})
    if not book:
        flash('Book not found!', 'danger')
        return redirect(url_for('home'))
    return render_template('reader.html', book=book)

# --- 7. AI SUMMARIZATION ---
@app.route("/book/<book_id>/generate_summary")
@login_required
def summarize_book(book_id):
    book = db.books.find_one({"_id": ObjectId(book_id)})
    if not book:
        return redirect(url_for('home'))
        
    content = book.get('content')
    if not content:
        flash('No text content found in this book.', 'warning')
        return redirect(url_for('book_details', book_id=book_id))
        
    # Run AI
    summary_text = generate_summary(content)
    
    db.books.update_one(
        {"_id": ObjectId(book_id)},
        {"$set": {"summary": summary_text}}
    )
    flash('AI Summary generated successfully!', 'success')
    return redirect(url_for('book_details', book_id=book_id))

# --- 8. READING LIST & RECOMMENDATIONS ---
@app.route("/book/<book_id>/save")
@login_required
def add_to_reading_list(book_id):
    db.users.update_one(
        {"_id": ObjectId(current_user.id)},
        {"$addToSet": {"saved_books": ObjectId(book_id)}}
    )
    flash('Book added to your Reading List!', 'success')
    return redirect(url_for('book_details', book_id=book_id))

@app.route("/book/<book_id>/remove")
@login_required
def remove_from_reading_list(book_id):
    db.users.update_one(
        {"_id": ObjectId(current_user.id)},
        {"$pull": {"saved_books": ObjectId(book_id)}}
    )
    flash('Book removed from your Reading List.', 'info')
    return redirect(url_for('book_details', book_id=book_id))

@app.route("/my_library")
@login_required
def my_library():
    # Get User's Saved Books
    user = db.users.find_one({"_id": ObjectId(current_user.id)})
    saved_ids = user.get('saved_books', [])
    
    my_books = []
    if saved_ids:
        my_books = list(db.books.find({"_id": {"$in": saved_ids}}))
    
    # Get AI Recommendations based on saved books
    all_books = list(db.books.find({"status": "approved"}))
    recommendations = get_recommendations(my_books, all_books)
    
    return render_template('my_library.html', books=my_books, recommendations=recommendations)

# --- 9. ADMIN PANEL ---
@app.route("/admin")
@login_required
def admin_panel():
    if current_user.role != 'Admin':
        flash('Access Denied. Admins only.', 'danger')
        return redirect(url_for('home'))
    
    pending_books = list(db.books.find({"status": "pending"}))
    return render_template('admin_panel.html', books=pending_books)

@app.route("/admin/approve/<book_id>")
@login_required
def approve_book(book_id):
    if current_user.role != 'Admin':
        return redirect(url_for('home'))
    db.books.update_one(
        {"_id": ObjectId(book_id)},
        {"$set": {"status": "approved"}}
    )
    flash('Book approved! It is now live.', 'success')
    return redirect(url_for('admin_panel'))

@app.route("/admin/reject/<book_id>")
@login_required
def reject_book(book_id):
    if current_user.role != 'Admin':
        return redirect(url_for('home'))
    db.books.delete_one({"_id": ObjectId(book_id)})
    flash('Book rejected and removed.', 'warning')
    return redirect(url_for('admin_panel'))