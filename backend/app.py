from flask import Flask, render_template, request, redirect, session, flash, url_for
from config import get_db_connection
import hashlib

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

app.secret_key = "adindiahub_secret_key"

import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="adindiahub_db"
    )

db = get_db_connection()
cursor = db.cursor()


@app.route("/")
def home():
    return render_template("home.html")
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        query = "INSERT INTO contact_messages (name, email, message) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, message))
        db.commit()

        return redirect("/contact")

    return render_template("contact.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/choose-login")
def choose_login():
    return render_template("choose_login.html")



# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["role"] = user["role"]

            if user["role"] == "admin":
                return redirect("/admin-dashboard")
            else:
                return redirect("/client-dashboard")
        else:
            return "Invalid login"

    return render_template("login.html")

# ---------------- REGISTER (CLIENT ONLY) ----------------
@app.route("/client-register", methods=["GET", "POST"])
def client_register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO clients (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )

        db.commit()
        cursor.close()
        db.close()

        return redirect("/client-login")

    return render_template("client_register.html")
 


# ---------------- ADMIN DASHBOARD ----------------
@app.route("/admin-dashboard")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect("/login")
    return render_template("admin_dashboard.html")

@app.route("/admin/messages")
def admin_messages():
    cursor.execute("SELECT * FROM contact_messages ORDER BY created_at DESC")
    messages = cursor.fetchall()
    return render_template("admin_messages.html", messages=messages)



@app.route("/client/login", methods=["GET", "POST"])
def client_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM clients WHERE email=%s AND password=%s",
            (email, password)
        )

        client = cursor.fetchone()

        cursor.close()
        conn.close()

        if client:
            session["client_id"] = client["id"]
            session["role"] = "client"
            flash("Login successful ✅")
            return redirect("/client-dashboard")
        else:
            flash("Invalid credentials ❌")

    return render_template("client_login.html")

# ---------------- CLIENT DASHBOARD ----------------
@app.route("/client-dashboard")
def client_dashboard():
    if session.get("role") != "client":
        return redirect("/client-login")

    client_id = session.get("client_id")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT campaign_name, platform, budget, start_date, end_date, status
        FROM campaigns
        WHERE client_id = %s
    """, (client_id,))

    campaigns = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("client_dashboard.html", campaigns=campaigns)

@app.route("/request-campaign", methods=["GET", "POST"])
def request_campaign():
    if session.get("role") != "client":
        return redirect("/client-login")

    if request.method == "POST":
        client_id = session.get("client_id")
        campaign_name = request.form["campaign_name"]
        platform = request.form["platform"]
        budget = request.form["budget"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        message = request.form["message"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO campaign_requests
            (client_id, campaign_name, platform, budget, start_date, end_date, message)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (client_id, campaign_name, platform, budget, start_date, end_date, message))

        conn.commit()
        cursor.close()
        conn.close()

        flash("Campaign request sent successfully ✅")
        return redirect("/client-dashboard")

    return render_template("request_campaign.html")

@app.route("/my-campaign-requests")
def my_campaign_requests():
    if session.get("role") != "client":
        return redirect("/client-login")

    client_id = session.get("client_id")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT campaign_name, platform, budget, start_date, end_date, status
        FROM campaign_requests
        WHERE client_id = %s
        ORDER BY request_id DESC
    """, (client_id,))

    requests = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("my_campaign_requests.html", requests=requests)

@app.route("/admin-campaign-requests")
def admin_campaign_requests():
    if session.get("role") != "admin":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            cr.request_id,
            cr.campaign_name,
            cr.platform,
            cr.budget,
            cr.start_date,
            cr.end_date,
            cr.status,
            cl.name AS client_name
        FROM campaign_requests cr
        JOIN clients cl ON cr.client_id = cl.id
        ORDER BY cr.request_id DESC
    """)

    requests = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("admin_campaign_requests.html", requests=requests)

@app.route("/approve-request/<int:request_id>")
def approve_request(request_id):
    if session.get("role") != "admin":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # get request data
    cursor.execute(
        "SELECT * FROM campaign_requests WHERE request_id=%s",
        (request_id,)
    )
    req = cursor.fetchone()

    # insert into campaigns
    cursor.execute("""
        INSERT INTO campaigns
        (client_id, campaign_name, platform, budget, start_date, end_date, status)
        VALUES (%s, %s, %s, %s, %s, %s, 'Active')
    """, (
        req["client_id"],
        req["campaign_name"],
        req["platform"],
        req["budget"],
        req["start_date"],
        req["end_date"]
    ))

    # update request status
    cursor.execute(
        "UPDATE campaign_requests SET status='Approved' WHERE request_id=%s",
        (request_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    flash("Campaign Approved & Created ✅")
    return redirect("/admin-campaign-requests")

@app.route("/reject-request/<int:request_id>")
def reject_request(request_id):
    if session.get("role") != "admin":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE campaign_requests SET status='Rejected' WHERE request_id=%s",
        (request_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    flash("Campaign Request Rejected ❌")
    return redirect("/admin-campaign-requests")


@app.route("/client/logout")
def client_logout():
    session.clear()
    return redirect("/")


# ---------------- ADD CAMPAIGN (ADMIN ONLY) ----------------
@app.route("/add-campaign", methods=["GET", "POST"])
def add_campaign():
    if session.get("role") != "admin":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, name FROM clients")
    clients = cursor.fetchall()

    if request.method == "POST":
        client_id = request.form["client_id"]
        campaign_name = request.form["campaign_name"]
        platform = request.form["platform"]
        budget = request.form["budget"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        cursor.execute("""
            INSERT INTO campaigns
            (client_id, campaign_name, platform, budget, start_date, end_date, status)
            VALUES (%s, %s, %s, %s, %s, %s, 'Active')
        """, (client_id, campaign_name, platform, budget, start_date, end_date))

        conn.commit()
        cursor.close()
        conn.close()

        flash("Campaign added successfully ✅")
        return redirect("/view-campaigns")

    cursor.close()
    conn.close()
    return render_template("add_campaign.html", clients=clients)

@app.route("/view-campaigns")
def view_campaigns():
    if session.get("role") != "admin":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            c.campaign_id,
            c.campaign_name,
            c.platform,
            c.budget,
            c.start_date,
            c.end_date,
            c.status,
            cl.name AS client_name
        FROM campaigns c
        JOIN clients cl ON c.client_id = cl.id
    """)

    campaigns = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("view_campaigns.html", campaigns=campaigns)

@app.route("/edit-campaign/<int:id>", methods=["GET", "POST"])
def edit_campaign(id):
    if session.get("role") != "admin":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM campaigns WHERE campaign_id = %s", (id,))
    campaign = cursor.fetchone()

    if request.method == "POST":
        campaign_name = request.form["campaign_name"]
        platform = request.form["platform"]
        budget = request.form["budget"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        status = request.form["status"]

        cursor.execute("""
            UPDATE campaigns SET
                campaign_name=%s,
                platform=%s,
                budget=%s,
                start_date=%s,
                end_date=%s,
                status=%s
            WHERE campaign_id=%s
        """, (campaign_name, platform, budget, start_date, end_date, status, id))

        conn.commit()
        cursor.close()
        conn.close()

        flash("Campaign updated successfully ✅")
        return redirect("/view-campaigns")

    cursor.close()
    conn.close()
    return render_template("edit_campaign.html", campaign=campaign)

@app.route("/delete-campaign/<int:id>")
def delete_campaign(id):
    if session.get("role") != "admin":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM campaigns WHERE campaign_id=%s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    flash("Campaign deleted successfully ❌")
    return redirect("/view-campaigns")


# ---------------- ADD CLIENT (ADMIN ONLY) ----------------
@app.route("/add-client", methods=["GET", "POST"])
def add_client():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        company_name = request.form["company_name"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO clients (name, email, phone, company_name) VALUES (%s, %s, %s, %s)",
            (name, email, phone, company_name)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/admin-dashboard")

    return render_template("add_client.html")



# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

