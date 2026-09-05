# app.py — the main program that runs the FILMO website.
#
# FILMO is a talent showcase. PERFORMERS build a profile and put videos of
# their talent on it. FILM MAKERS browse those profiles and watch the videos
# to find people for their projects. An ADMIN decides which film makers are
# allowed in, and keeps an eye on everybody.

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from firebase_config import db   # our database connection

app = Flask(__name__)

# A "secret key" lets Flask keep users securely logged in (called a session).
# It is a long random string. Flask uses it to sign the cookie in the visitor's
# browser, so nobody can edit that cookie and pretend to be someone else.
app.secret_key = "a5eb07daec495678632155028981cc6789796dc31b990317"

# Used to fill the gender dropdown on the performer sign-up form.
GENDERS = ["Male", "Female", "Other"]

# Used to fill the dropdown when a performer adds a talent video.
TALENT_CATEGORIES = ["Acting", "Dancing", "Singing", "Music", "Comedy",
                     "Stunts / Action", "Modelling", "Other"]


def now_iso():
    """Current date & time as text."""
    return datetime.now(timezone.utc).isoformat()


def require_role(role):
    """If the visitor is NOT logged in with this role, return a redirect to send them away.
    If they ARE allowed, return None. Used at the top of protected pages."""
    if session.get("role") != role:
        flash("Please log in as " + role + " to view that page.", "warning")
        return redirect(url_for("login"))
    return None


def users_with_role(role, status=None):
    """Fetch every user of one role — for example all performers, or only the
    film makers who are still 'pending'. Newest first."""
    found = []
    for doc in db.collection("users").stream():
        u = doc.to_dict()
        if u.get("role") != role:
            continue
        if status is not None and u.get("status") != status:
            continue
        found.append(u)
    found.sort(key=lambda u: u.get("created_at", ""), reverse=True)
    return found


def get_talents(user_email=None):
    """Fetch talent videos, newest first. Pass an email for just one performer's."""
    found = []
    for doc in db.collection("talents").stream():
        t = doc.to_dict()
        if user_email is not None and t.get("user_email") != user_email:
            continue
        t["id"] = doc.id       # remember the document id so pages can link to it
        found.append(t)
    found.sort(key=lambda t: t.get("created_at", ""), reverse=True)
    return found


def looks_like_link(text):
    """A light check that the pasted video address is a real web link."""
    return text.startswith("http://") or text.startswith("https://")


@app.template_filter("nice_date")
def nice_date(value):
    """Used in pages as {{ some_date | nice_date }}. Turns a stored timestamp
    like '2026-09-04T14:20:00+00:00' into the friendlier '04 Sep 2026'."""
    if not value:
        return "-"
    try:
        return datetime.fromisoformat(value).strftime("%d %b %Y")
    except ValueError:
        return value


# ================= PUBLIC PAGES =================
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register")
def register_choice():
    """A small page that asks: are you a film maker, or a performer?"""
    return render_template("register_choice.html")


@app.route("/register/user", methods=["GET", "POST"])
def register_user():
    """Sign-up form for performers (the people showing off their talent)."""
    if request.method == "POST":
        email = request.form["email"].strip().lower()

        # Email is the document id, so it must be unique.
        if db.collection("users").document(email).get().exists:
            flash("An account with this email already exists. Please log in.", "warning")
            return redirect(url_for("login"))

        db.collection("users").document(email).set({
            "name": request.form["name"].strip(),
            "email": email,
            "password": generate_password_hash(request.form["password"]),
            "phone": request.form["phone"].strip(),
            "age": request.form["age"].strip(),
            "gender": request.form["gender"],
            "skills": request.form["skills"].strip(),
            "city": request.form["city"].strip(),
            "bio": request.form["bio"].strip(),
            "role": "user",
            "created_at": now_iso(),
        })
        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register_user.html", genders=GENDERS)


@app.route("/register/filmmaker", methods=["GET", "POST"])
def register_filmmaker():
    """Sign-up form for film makers. They start as 'pending' and cannot log in
    until an admin approves them."""
    if request.method == "POST":
        email = request.form["email"].strip().lower()

        if db.collection("users").document(email).get().exists:
            flash("An account with this email already exists. Please log in.", "warning")
            return redirect(url_for("login"))

        db.collection("users").document(email).set({
            "name": request.form["name"].strip(),
            "email": email,
            "password": generate_password_hash(request.form["password"]),
            "phone": request.form["phone"].strip(),
            "company": request.form["company"].strip(),
            "experience": request.form["experience"].strip(),
            "city": request.form["city"].strip(),
            "role": "filmmaker",
            "status": "pending",     # waiting for the admin to accept or reject
            "created_at": now_iso(),
        })
        flash("Request sent! An admin will review your film maker account soon.", "success")
        return redirect(url_for("login"))

    return render_template("register_filmmaker.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        user_doc = db.collection("users").document(email).get()
        if not user_doc.exists:
            flash("No account found with that email.", "danger")
            return redirect(url_for("login"))

        user = user_doc.to_dict()
        if not check_password_hash(user["password"], password):
            flash("Incorrect password. Please try again.", "danger")
            return redirect(url_for("login"))

        # Film makers must be approved by the admin before they are let in.
        if user["role"] == "filmmaker":
            status = user.get("status", "pending")
            if status == "pending":
                flash("Your film maker account is still waiting for admin approval. "
                      "Please try again later.", "warning")
                return redirect(url_for("login"))
            if status == "rejected":
                flash("Sorry — your film maker request was rejected by the admin.", "danger")
                return redirect(url_for("login"))

        session["email"] = email
        session["name"] = user["name"]
        session["role"] = user["role"]
        flash("Welcome back, " + user["name"] + "!", "success")

        # Sends admin -> admin_dashboard, filmmaker -> filmmaker_dashboard, user -> user_dashboard
        return redirect(url_for(user["role"] + "_dashboard"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))


# ================= A PERFORMER'S PROFILE (seen by others) =================
@app.route("/performer/<email>")
def view_performer(email):
    """One performer's details and all their talent videos.
    Film makers and the admin may both open this page."""
    if session.get("role") not in ("filmmaker", "admin"):
        flash("Please log in as a film maker to view performer profiles.", "warning")
        return redirect(url_for("login"))

    user_doc = db.collection("users").document(email).get()
    if not user_doc.exists or user_doc.to_dict().get("role") != "user":
        flash("That performer was not found.", "danger")
        # Send each kind of visitor back to their own list of performers.
        if session.get("role") == "admin":
            return redirect(url_for("admin_users"))
        return redirect(url_for("filmmaker_performers"))

    return render_template("view_performer.html",
                           performer=user_doc.to_dict(),
                           talents=get_talents(user_email=email))


# ================= PERFORMER (USER) MODULE =================
@app.route("/user/dashboard")
def user_dashboard():
    guard = require_role("user")
    if guard:
        return guard

    my_talents = get_talents(user_email=session["email"])
    return render_template("user_dashboard.html", talent_count=len(my_talents))


@app.route("/profile", methods=["GET", "POST"])
def profile():
    """The performer views and edits their own details.
    Email and role can't be changed — email is the key we look them up by."""
    guard = require_role("user")
    if guard:
        return guard

    user_ref = db.collection("users").document(session["email"])

    # Saving changes.
    if request.method == "POST":
        new_name = request.form["name"].strip()
        if not new_name:
            flash("Your name can't be empty.", "danger")
            return redirect(url_for("profile"))

        user_ref.update({
            "name": new_name,
            "phone": request.form["phone"].strip(),
            "age": request.form["age"].strip(),
            "gender": request.form["gender"],
            "skills": request.form["skills"].strip(),
            "city": request.form["city"].strip(),
            "bio": request.form["bio"].strip(),
        })
        session["name"] = new_name    # keep the greeting in the top bar up to date
        flash("Your profile has been updated.", "success")
        return redirect(url_for("profile"))

    # Showing the current details.
    return render_template("profile.html", user=user_ref.get().to_dict(), genders=GENDERS)


@app.route("/user/talents")
def user_talents():
    """The performer's own showreel — the talent videos on their profile."""
    guard = require_role("user")
    if guard:
        return guard
    return render_template("user_talents.html",
                           talents=get_talents(user_email=session["email"]))


@app.route("/user/talents/add", methods=["GET", "POST"])
def user_talent_add():
    """Add a talent video by pasting its YouTube or Google Drive link."""
    guard = require_role("user")
    if guard:
        return guard

    if request.method == "POST":
        title = request.form["title"].strip()
        video_url = request.form["video_url"].strip()

        if not title:
            flash("Please give your video a title.", "danger")
            return redirect(url_for("user_talent_add"))
        if not looks_like_link(video_url):
            flash("Please paste a full video link starting with http:// or https://", "danger")
            return redirect(url_for("user_talent_add"))

        db.collection("talents").add({
            "user_email": session["email"],
            "user_name": session["name"],
            "title": title,
            "category": request.form["category"],
            "description": request.form["description"].strip(),
            "video_url": video_url,
            "created_at": now_iso(),
        })
        flash("Talent video added! Film makers can now see it on your profile. ⭐", "success")
        return redirect(url_for("user_talents"))

    return render_template("user_talent_add.html", categories=TALENT_CATEGORIES)


@app.route("/user/talents/<talent_id>/delete", methods=["POST"])
def user_talent_delete(talent_id):
    """Remove one of your own talent videos."""
    guard = require_role("user")
    if guard:
        return guard

    talent_ref = db.collection("talents").document(talent_id)
    talent_doc = talent_ref.get()
    if not talent_doc.exists:
        flash("That video was not found.", "danger")
    elif talent_doc.to_dict().get("user_email") != session["email"]:
        flash("You can only remove your own videos.", "danger")
    else:
        talent_ref.delete()
        flash("Video removed.", "info")

    return redirect(url_for("user_talents"))


# ================= FILM MAKER MODULE =================
@app.route("/filmmaker/dashboard")
def filmmaker_dashboard():
    guard = require_role("filmmaker")
    if guard:
        return guard

    return render_template("filmmaker_dashboard.html",
                           performer_count=len(users_with_role("user")),
                           video_count=len(get_talents()))


@app.route("/filmmaker/performers")
def filmmaker_performers():
    """Every performer on FILMO, so a film maker can go and watch their videos."""
    guard = require_role("filmmaker")
    if guard:
        return guard
    return render_template("filmmaker_performers.html", performers=users_with_role("user"))


# ================= ADMIN MODULE =================
@app.route("/admin/dashboard")
def admin_dashboard():
    guard = require_role("admin")
    if guard:
        return guard

    # Read the users once, then count the different kinds.
    users = [u.to_dict() for u in db.collection("users").stream()]
    pending_requests = sum(1 for u in users
                           if u.get("role") == "filmmaker" and u.get("status") == "pending")
    approved_makers = sum(1 for u in users
                          if u.get("role") == "filmmaker" and u.get("status") == "approved")
    performers = sum(1 for u in users if u.get("role") == "user")

    return render_template("admin_dashboard.html",
                           pending_requests=pending_requests,
                           approved_makers=approved_makers,
                           performers=performers,
                           total_talents=len(get_talents()))


@app.route("/admin/filmmaker-requests")
def admin_filmmaker_requests():
    """Film makers waiting to be let in — plus any the admin rejected earlier."""
    guard = require_role("admin")
    if guard:
        return guard
    return render_template("admin_filmmaker_requests.html",
                           pending=users_with_role("filmmaker", "pending"),
                           rejected=users_with_role("filmmaker", "rejected"))


@app.route("/admin/filmmaker-requests/<email>/<action>", methods=["POST"])
def admin_handle_filmmaker(email, action):
    """Runs when the admin presses Accept or Reject on a film maker request."""
    guard = require_role("admin")
    if guard:
        return guard

    maker_ref = db.collection("users").document(email)
    maker_doc = maker_ref.get()
    if not maker_doc.exists:
        flash("That film maker was not found.", "danger")
        return redirect(url_for("admin_filmmaker_requests"))

    name = maker_doc.to_dict().get("name", "The film maker")

    if action == "accept":
        maker_ref.update({"status": "approved"})
        flash(name + " has been approved and can now log in.", "success")
    elif action == "reject":
        maker_ref.update({"status": "rejected"})
        flash(name + " has been rejected.", "info")
    else:
        flash("Unknown action.", "danger")

    return redirect(url_for("admin_filmmaker_requests"))


@app.route("/admin/filmmakers")
def admin_filmmakers():
    guard = require_role("admin")
    if guard:
        return guard
    return render_template("admin_filmmakers.html",
                           filmmakers=users_with_role("filmmaker", "approved"))


@app.route("/admin/users")
def admin_users():
    """Every registered performer. Each row links to their profile and videos."""
    guard = require_role("admin")
    if guard:
        return guard
    return render_template("admin_users.html", users=users_with_role("user"))


# ================= FRIENDLY ERROR PAGES =================
# Without these, a mistyped address shows a bare white page from Flask.
@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html",
                           code=404,
                           heading="We couldn't find that page",
                           message="The address may have been typed wrong, or the "
                                   "page may have moved."), 404


@app.errorhandler(500)
def something_broke(error):
    return render_template("error.html",
                           code=500,
                           heading="Something went wrong on our side",
                           message="Sorry about that. Please try again in a moment."), 500


# ================= START THE WEBSITE =================
if __name__ == "__main__":
    # Port 5001 (not the usual 5000) so FILMO can run at the same time as the
    # Blood Bank project without the two clashing over the same address.
    app.run(debug=True, port=5001)
