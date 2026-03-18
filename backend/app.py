import os
from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
from werkzeug.utils import secure_filename

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

#   ---------------- HOME PAGE ----------------

@app.route("/")
def home():
    return render_template("home.html")

# ---------------- CONTACT PAGE ----------------

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        conn = get_db_connection()
        cursor = conn.cursor()

        query = "INSERT INTO contact_messages (name, email, message) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, message))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect("/contact")

    return render_template("contact.html")

# Upload folder setup
UPLOAD_FOLDER = os.path.join(app.static_folder, "ads_videos")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


UPLOAD_FOLDER = os.path.join(app.static_folder, "profile_photos")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- ABOUT PAGE ----------------

@app.route("/about")
def about():
    return render_template("about.html")



# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # First check Admin
        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )
        admin = cursor.fetchone()

        if admin:
            session["user_id"] = admin["id"]
            session["role"] = "admin"
            cursor.close()
            conn.close()
            return redirect("/admin-dashboard")

        # Then check Client
        cursor.execute(
            "SELECT * FROM clients WHERE email=%s AND password=%s",
            (email, password)
        )
        client = cursor.fetchone()

        if client:
            session["client_id"] = client["id"]
            session["role"] = "client"
            cursor.close()
            conn.close()
            return redirect("/client-dashboard")

        cursor.close()
        conn.close()
        flash("Invalid Email or Password ❌")
        return redirect("/login")

    return render_template("login.html")


# ---------------- REGISTER (CLIENT ONLY) ----------------

@app.route("/register", methods=["GET", "POST"])
def client_register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Passwords do not match ❌")
            return redirect("/register")

        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO clients (name, email, phone, password) VALUES (%s, %s, %s, %s)",
            (name, email, phone, password)
        )

        db.commit()
        cursor.close()
        db.close()

        flash("Registration successful! Please login ✅")
        return redirect("/login")

    return render_template("register.html")

# ---------------- ADMIN DASHBOARD ----------------

@app.route("/admin-dashboard")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total_clients FROM clients")
    total_clients = cursor.fetchone()["total_clients"]

    cursor.execute("SELECT COUNT(*) AS total_campaigns FROM campaigns")
    total_campaigns = cursor.fetchone()["total_campaigns"]

    cursor.execute("SELECT COUNT(*) AS active_campaigns FROM campaigns WHERE status='Active'")
    active_campaigns = cursor.fetchone()["active_campaigns"]

    cursor.execute("SELECT COUNT(*) AS pending_requests FROM campaign_requests WHERE status='Pending'")
    pending_requests = cursor.fetchone()["pending_requests"]

    cursor.execute("SELECT COUNT(*) AS rejected_requests FROM campaign_requests WHERE status='Rejected'")
    rejected_requests = cursor.fetchone()["rejected_requests"]

    video_count = len(os.listdir(app.config["UPLOAD_FOLDER"]))

    cursor.close()
    conn.close()

    return render_template(
        "admin_dashboard.html",
        total_clients=total_clients,
        total_campaigns=total_campaigns,
        active_campaigns=active_campaigns,
        pending_requests=pending_requests,
        rejected_requests=rejected_requests,
        video_count=video_count
    )

# ---------------- UPLOAD AD VIDEO (ADMIN ONLY) ----------------

@app.route("/upload-ad-video", methods=["GET", "POST"])
def upload_ad_video():
    if request.method == "POST":
        if "ad_video" not in request.files:
            flash("No file selected")
            return redirect(request.url)

        file = request.files["ad_video"]

        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)

        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(save_path)

        flash("Ad video uploaded successfully!")
        return redirect(url_for("admin_dashboard"))

    return render_template("upload_ad.html")


# Route for platform page
@app.route('/platform')
def platform():
    return render_template('adindiahub_platform.html')

# ---------------- VIEW CLIENTS (ADMIN ONLY) ----------------

@app.route("/view-clients")
def view_clients():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clients")
    clients = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("view_clients.html", clients=clients)

# ---------------- ADMIN VIDEOS ----------------

@app.route("/admin/videos")
def admin_videos():
    video_folder = app.config["UPLOAD_FOLDER"]
    videos = os.listdir(video_folder)
    return render_template("admin_videos.html", videos=videos)

# ---------------- ADMIN MESSAGES ----------------

@app.route("/admin/messages")
def admin_messages():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM contact_messages ORDER BY created_at DESC")
    messages = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("admin_messages.html", messages=messages)

# ---------------- CLIENT LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
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
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session["client_id"] = user["id"]
            session["role"] = "client"
            return redirect("/client-dashboard")
        else:
            return render_template("login.html", error="Invalid Email or Password")

    return render_template("login.html")



# ---------------- CLIENT DASHBOARD ----------------

@app.route("/client-dashboard")
def client_dashboard():
    if session.get("role") != "client":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 🔹 Client profile (name + photo)
    cursor.execute(
        "SELECT name, profile_photo FROM clients WHERE id=%s",
        (session["client_id"],)
    )
    client = cursor.fetchone()

    # 🔹 Client campaigns
    cursor.execute("""
        SELECT campaign_id, campaign_name, platform, budget,
               start_date, end_date, status, ad_video
        FROM campaigns
        WHERE client_id=%s AND status='Active'
    """, (session["client_id"],))

    campaigns = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "client_dashboard.html",
        client=client,
        campaigns=campaigns
    )
# ---------------- EDIT PROFILE (CLIENT ONLY) ----------------

import os
from werkzeug.utils import secure_filename

@app.route("/edit-profile", methods=["GET", "POST"])
def edit_profile():
    if session.get("role") != "client":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 🔹 GET client data
    cursor.execute(
        "SELECT id, name, profile_photo FROM clients WHERE id=%s",
        (session["client_id"],)
    )
    client = cursor.fetchone()

    if request.method == "POST":
        name = request.form.get("name")
        photo = request.files.get("photo")

        photo_filename = client["profile_photo"]

        # 🔹 Upload folder
        UPLOAD_FOLDER = os.path.join(
            app.root_path, "frontend", "static", "profile_photos"
        )
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        # 🔹 If new photo uploaded
        if photo and photo.filename != "":
            photo_filename = secure_filename(photo.filename)
            photo.save(os.path.join(UPLOAD_FOLDER, photo_filename))

        # 🔹 Update DB
        cursor.execute("""
            UPDATE clients
            SET name=%s, profile_photo=%s
            WHERE id=%s
        """, (name, photo_filename, session["client_id"]))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/client-dashboard")

    cursor.close()
    conn.close()

    return render_template("edit_profile.html", client=client)

# ---------------- REQUEST CAMPAIGN (CLIENT ONLY) ----------------

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

#  ---------------- MY CAMPAIGN REQUESTS (CLIENT ONLY) ----------------

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

# ---------------- SUBMIT FEEDBACK (CLIENT ONLY) ----------------

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    campaign_id = request.form.get('campaign_id')
    stars = request.form.get('stars')
    comment = request.form.get('comment')
    client_id = session.get('client_id')

    print(campaign_id, stars, comment)  # DEBUG

    conn = mysql.connector.connect(host="localhost", user="root", password="", database="adindiahub_db")
    cur = conn.cursor()

    cur.execute("INSERT INTO video_feedback (campaign_id, client_id, stars, comment) VALUES (%s,%s,%s,%s)",
                (campaign_id, client_id, stars, comment))

    conn.commit()
    cur.close()
    conn.close()

    return redirect('/client-dashboard')

# ---------------- DELETE CAMPAIGN (CLIENT) ----------------

@app.route("/delete-my-campaign/<int:campaign_id>")
def delete_my_campaign(campaign_id):
    if session.get("role") != "client":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM campaigns
        WHERE campaign_id = %s AND client_id = %s
    """, (campaign_id, session["client_id"]))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/client-dashboard")




# ---------------- ADMIN CAMPAIGN REQUESTS ----------------

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

    # video list
    video_folder = app.config["UPLOAD_FOLDER"]
    videos = os.listdir(video_folder)


    cursor.close()
    conn.close()

    return render_template("admin_campaign_requests.html", requests=requests, videos=videos)

# ---------------- VIEW CAMPAIGNS (ADMIN ONLY) ----------------

@app.route("/campaign-list")
def campaign_list():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT 
         id,
        campaigns.campaign_name,
        clients.name AS client_name,
        campaigns.platform,
        campaigns.budget,
        campaigns.status
    FROM campaigns
    JOIN clients ON campaigns.client_id = clients.id
    """

    cursor.execute(query)
    campaigns = cursor.fetchall()
    conn.close()

    return render_template("campaign_list.html", campaigns=campaigns)

import os

UPLOAD_FOLDER = app.config["UPLOAD_FOLDER"]

# ---------------- VIEW FEEDBACK (ADMIN ONLY) ----------------

@app.route('/view-feedback')
def view_feedback():
    conn =  get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT vf.stars, vf.comment, c.campaign_name, cl.name
        FROM video_feedback vf
        JOIN campaigns c ON vf.campaign_id = c.campaign_id
        JOIN clients cl ON vf.client_id = cl.id
        ORDER BY vf.created_at DESC
    """)
    
    feedbacks = cur.fetchall()
    return render_template("admin_feedback.html", feedbacks=feedbacks)


# ---------------- APPROVE REQUEST ----------------

@app.route("/approve-request/<int:request_id>")
def approve_request(request_id):
    if session.get("role") != "admin":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE campaign_requests SET status='Approved' WHERE request_id=%s",
        (request_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    flash("Campaign approved  Now assign video")
    return redirect("/admin-campaign-requests")

# ---------------- REJECT REQUEST ----------------

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

    flash("Campaign Request Rejected ")
    return redirect("/admin-campaign-requests")

# ---------------- ASSIGN VIDEO TO APPROVED REQUEST ----------------

@app.route("/assign-video/<int:request_id>", methods=["POST"])
def assign_video(request_id):
    if session.get("role") != "admin":
        return redirect("/login")

    ad_video = request.form.get("ad_video")

    if not ad_video:
        flash("Please select a video ")
        return redirect("/admin-campaign-requests")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM campaign_requests WHERE request_id=%s",
        (request_id,)
    )
    req = cursor.fetchone()

    cursor.execute("""
        INSERT INTO campaigns
        (client_id, campaign_name, platform, budget,
         start_date, end_date, status, ad_video)
        VALUES (%s,%s,%s,%s,%s,%s,'Active',%s)
    """, (
        req["client_id"],
        req["campaign_name"],
        req["platform"],
        req["budget"],
        req["start_date"],
        req["end_date"],
        ad_video
    ))

    cursor.execute(
        "UPDATE campaign_requests SET status='Assigned' WHERE request_id=%s",
        (request_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    flash("Campaign approved with video ")
    return redirect("/admin-campaign-requests")

# ---------------- ADMIN CAMPAIGNS ----------------

@app.route("/admin-campaigns")
def admin_campaigns():
    if session.get("role") != "admin":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT c.campaign_id, c.campaign_name, c.platform, c.budget,
               c.status, c.ad_video, cl.name AS client_name
        FROM campaigns c
        JOIN clients cl ON c.client_id = cl.id
        ORDER BY c.campaign_id DESC
    """)
    campaigns = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template("admin_campaigns.html", campaigns=campaigns)

# ---------------- CLIENT LOGOUT ----------------
@app.route("/client/logout")
def client_logout():
    session.clear()
    return redirect("/")

# ---------------- VIEW CAMPAIGNS (ADMIN ONLY) ----------------

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

# ---------------- EDIT CAMPAIGN (ADMIN ONLY) ----------------

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

        flash("Campaign updated successfully ")
        return redirect("/view-campaigns")

    cursor.close()
    conn.close()
    return render_template("edit_campaign.html", campaign=campaign)

# ---------------- DELETE CAMPAIGN (ADMIN ONLY) ----------------
@app.route("/delete-campaign/<int:campaign_id>")
def delete_campaign(campaign_id):
    if session.get("role") != "admin":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM campaigns WHERE campaign_id = %s",
        (campaign_id,)
    )
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/view-campaigns")



# ---------------- client profile ----------------

@app.route('/client-profile')
def client_profile():
    if 'client_id' not in session:
        return redirect('/login')

    client_id = session['client_id']
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clients WHERE id=%s", (client_id,))
    client = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("client_profile.html", client=client)




# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)