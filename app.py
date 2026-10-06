from flask import Flask, render_template, request, redirect, session, url_for, make_response, jsonify
import sqlite3
from database import init_db, save_user, verify_user
from jwt_handler import generate_token, token_required
from rag_engine import process_ticket_pipeline

# 1. Initialize Flask app
app = Flask(__name__)
app.secret_key = "supportpilot_secret_key"

# Initialize database tables
init_db()

# 2. Root Route -> Opens register.html first
@app.route("/")
def home():
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        # Verify credentials against SQLite database users table
        conn = sqlite3.connect("support_pilot.db")
        cursor = conn.cursor()
        cursor.execute("SELECT full_name, email FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            # Generate JWT token upon successful authentication
            token = generate_token(user[0], user[1])
            
            # Save token inside HTTP-only cookie and redirect to dashboard
            resp = make_response(redirect(url_for("dashboard")))
            resp.set_cookie("auth_token", token, httponly=True)
            return resp
        else:
            error = "Invalid email or password. Please try again."
            
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    # Clear JWT cookie to end session
    resp = make_response(redirect(url_for("login")))
    resp.set_cookie("auth_token", "", expires=0)
    return resp

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("fullName")
        email = request.form.get("email")
        department = request.form.get("department")
        password = request.form.get("password")
        
        success = save_user(full_name, email, department, password)
        if success:
            # Generate JWT token immediately upon registration and log them in
            token = generate_token(full_name, email)
            resp = make_response(redirect(url_for("dashboard")))
            resp.set_cookie("auth_token", token, httponly=True)
            return resp
        else:
            return "Email already registered or error occurred!", 400
            
    return render_template("register.html")

# 3. Dashboard and Tickets Workspace Routes
@app.route("/dashboard")
@token_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/tickets", methods=["GET", "POST"])
@token_required
def tickets():
    if request.method == "POST":
        data = request.get_json() if request.is_json else request.form
        category = data.get("category", "Returns & Refunds")
        query_text = data.get("ticket_query", "")
        
        # Run RAG & Validation Pipeline
        result = process_ticket_pipeline(category, query_text)
        return jsonify(result)
        
    return render_template("tickets.html")

@app.route("/dispatch-ticket", methods=["POST"])
@token_required
def dispatch_ticket():
    data = request.get_json() if request.is_json else request.form
    customer_email = data.get("email")
    order_ref = data.get("order_ref")
    resolution_text = data.get("resolution")
    
    # Optional: Save dispatch record to SQLite database
    try:
        conn = sqlite3.connect("support_pilot.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dispatches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT,
                order_ref TEXT,
                resolution TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute(
            "INSERT INTO dispatches (email, order_ref, resolution) VALUES (?, ?, ?)",
            (customer_email, order_ref, resolution_text)
        )
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Ticket successfully dispatched and logged!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)