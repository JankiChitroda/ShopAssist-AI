import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, redirect, session, url_for, make_response, jsonify
import sqlite3
from database import init_db, save_user, verify_user
from jwt_handler import generate_token, token_required
from rag_engine import process_ticket_pipeline
from jira_service import create_jira_ticket
from email_service import send_escalation_email, send_resolution_email

# 1. Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supportpilot_secret_key")

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
        customer_email = data.get("email", "").strip()
        order_ref = data.get("order_ref", "").strip()
        
        # Run RAG & Validation Pipeline with real customer identity data
        result = process_ticket_pipeline(category, query_text, customer_email=customer_email, order_ref=order_ref)
        return jsonify(result)
        
    return render_template("tickets.html")

@app.route("/dispatch-ticket", methods=["POST"])
@token_required
def dispatch_ticket():
    data = request.get_json() if request.is_json else request.form
    customer_email = data.get("email")
    order_ref = data.get("order_ref") or "#ORD-7741"
    resolution_text = data.get("resolution")
    category = data.get("category", "Returns & Refunds")
    query_text = data.get("query_text", "")
    
    from datetime import datetime
    created_at_str = datetime.now().strftime("%b %d, %Y, %I:%M %p")
    ticket_id = f"SHOP-RES-{str(order_ref).replace('#', '').replace('ORD-', '')}"
    
    ticket_details = {
        "ticket_id": ticket_id,
        "jira_key": ticket_id,
        "category": category,
        "priority": "Normal",
        "status": "Approved",
        "order_ref": order_ref,
        "customer_email": customer_email,
        "created_at": created_at_str,
        "query_text": query_text,
        "resolution": resolution_text
    }
    
    # 1. Send resolution email to customer via SMTP
    email_success = False
    try:
        email_success = send_resolution_email(customer_email, order_ref, resolution_text, ticket_details=ticket_details)
    except Exception as em_err:
        print(f"⚠️ Dispatch email failed: {em_err}")
    
    # 2. Save dispatch record to SQLite database
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
        return jsonify({
            "status": "success",
            "email_sent": email_success,
            "message": "Ticket successfully dispatched, logged, and resolution email sent to customer!"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/escalate-ticket", methods=["POST"])
@token_required
def escalate_ticket():
    data = request.get_json() if request.is_json else request.form
    customer_email = data.get("email", "")
    order_ref = data.get("order_ref", "") or "#ORD-7741"
    category = data.get("category", "Payment Dispute")
    query_text = data.get("query_text", "")
    resolution_text = data.get("resolution", "")
    customer_name = data.get("customer_name") or session.get("user_name") or "Yashwanth"
    
    # 1. Create live Jira Issue
    jira_summary = f"Escalated Support Ticket: {category} ({order_ref})"
    jira_desc = (
        f"Customer Query: {query_text}\n\n"
        f"Order Reference: {order_ref}\n"
        f"Customer Email: {customer_email}\n\n"
        f"AI Proposed Draft: {resolution_text}\n\n"
        f"Escalation Reason: Support agent manually escalated ticket to Tier-2 human review."
    )
    jira_result = create_jira_ticket(summary=jira_summary, description=jira_desc, priority="High")
    jira_key = jira_result.get("jira_key", "SHOP-1042") if isinstance(jira_result, dict) else "SHOP-1042"
    
    # 2. Build full real ticket details matching the template in the screenshot
    from datetime import datetime
    created_at_str = datetime.now().strftime("%b %d, %Y, %I:%M %p")
    jira_browse_url = f"{os.getenv('JIRA_URL', 'https://yashwanthaagunuri12.atlassian.net').rstrip('/')}/browse/{jira_key}"
    
    ticket_details = {
        "jira_key": jira_key,
        "category": category,
        "priority": "High",
        "order_ref": order_ref,
        "customer_email": customer_email or os.getenv("SMTP_EMAIL", "yashwanthaagunuri15@gmail.com"),
        "customer_name": customer_name,
        "created_at": created_at_str,
        "query_text": query_text,
        "resolution_draft": resolution_text,
        "jira_browse_url": jira_browse_url
    }

    # 3. Send live SMTP escalation alert email with rich ShopAssist template
    email_subject = f"Action Required: Your support ticket has been escalated [{jira_key}]"
    email_body = (
        f"Hello {customer_name},\n\n"
        f"Your support ticket has been escalated to Tier-2 review.\n\n"
        f"Ticket ID: {jira_key}\n"
        f"Category: {category}\n"
        f"Order Reference: {order_ref}\n"
        f"Priority: High\n\n"
        f"Query:\n{query_text}\n\n"
        f"Proposed Draft:\n{resolution_text}\n\n"
        f"View Ticket: {jira_browse_url}"
    )
    email_success = send_escalation_email(
        recipient_email=customer_email or "shopassist23@gmail.com",
        subject=email_subject,
        body=email_body,
        ticket_details=ticket_details
    )
    
    return jsonify({
        "status": "success",
        "jira_key": jira_key,
        "email_sent": email_success,
        "recipient": ticket_details["customer_email"],
        "ticket_details": ticket_details,
        "message": f"Successfully created Jira ticket {jira_key} and sent escalation email to {ticket_details['customer_email']}!"
    }), 200

if __name__ == "__main__":
    app.run(debug=True)