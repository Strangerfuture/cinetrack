import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, lookup

app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Database helper function
def get_db():
    conn = sqlite3.connect('personal.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.route("/")
@login_required
def index():
    # Show dashboard: Watched list and Watchlist
    conn = get_db()
    user_id = session["user_id"]
    
    # Get Reviews
    reviews = conn.execute("""
        SELECT m.title, m.poster, r.rating, r.review, r.watched_date 
        FROM reviews r 
        JOIN media m ON r.media_id = m.id 
        WHERE r.user_id = ? ORDER BY r.watched_date DESC
    """, (user_id,)).fetchall()

    # Get Watchlist
    watchlist = conn.execute("""
        SELECT m.title, m.poster, m.year, m.media_type 
        FROM watchlist w 
        JOIN media m ON w.media_id = m.id 
        WHERE w.user_id = ?
    """, (user_id,)).fetchall()
    
    conn.close()
    return render_template("index.html", reviews=reviews, watchlist=watchlist)


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "POST":
        query = request.form.get("query")
        if not query:
            return redirect("/search")
        
        results = lookup(query)
        return render_template("search.html", results=results, query=query)
    
    
    return render_template("search.html", results=[])


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    
    # 1. Get Data from Form
    tmdb_id = request.form.get("tmdb_id")
    title = request.form.get("title")
    media_type = request.form.get("media_type")
    poster = request.form.get("poster")
    year = request.form.get("year")
    action = request.form.get("action") # 'watchlist' or 'review'

    conn = get_db()
    cursor = conn.cursor()

    # 2. Ensure Media Exists in Local DB (Cache it)
    cursor.execute("SELECT id FROM media WHERE tmdb_id = ?", (tmdb_id,))
    media_row = cursor.fetchone()

    if media_row is None:
        cursor.execute("INSERT INTO media (tmdb_id, title, media_type, poster, year) VALUES (?, ?, ?, ?, ?)",
                       (tmdb_id, title, media_type, poster, year))
        media_id = cursor.lastrowid
    else:
        media_id = media_row["id"]

    # 3. Perform Action
    user_id = session["user_id"]

    if action == "watchlist":
        # Check if already in watchlist
        cursor.execute("SELECT id FROM watchlist WHERE user_id = ? AND media_id = ?", (user_id, media_id))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO watchlist (user_id, media_id) VALUES (?, ?)", (user_id, media_id))
            flash("Added to Watchlist!")
        else:
            flash("Already in Watchlist.")

    elif action == "review":
        rating = request.form.get("rating")
        review_text = request.form.get("review_text")
        cursor.execute("INSERT INTO reviews (user_id, media_id, rating, review) VALUES (?, ?, ?, ?)",
                       (user_id, media_id, rating, review_text))
        flash("Review logged!")

    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchone()
        conn.close()

        if not user or not check_password_hash(user["hash"], request.form.get("password")):
            return render_template("login.html", error="Invalid username or password")

        session["user_id"] = user["id"]
        return redirect("/")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username or not password:
            return render_template("register.html", error="Fields cannot be empty")

        hash_pw = generate_password_hash(password)
        conn = get_db()
        try:
            conn.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash_pw))
            conn.commit()
        except sqlite3.IntegrityError:
            return render_template("register.html", error="Username already taken")
        finally:
            conn.close()
            
        return redirect("/login")
    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
