import os
from datetime import datetime, date
from uuid import uuid4

import pymysql
from pymysql.cursors import DictCursor
from pymysql.err import IntegrityError

from flask import (
    Flask, render_template, request, redirect, url_for, session, flash, g, abort
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
from PIL import Image


load_dotenv()  # reads .env if present

APP_TITLE = "In JESUS NAME AMEN!!!"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-change-me")
app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER", "static/uploads")
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10MB

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

csrf = CSRFProtect(app)
limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])


def mysql_conn():
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("your_password", ""),
        database=os.getenv("MYSQL_DB", "prayer_app"),
        cursorclass=DictCursor,
        autocommit=False,
        charset="utf8mb4",
    )


def get_db():
    if "db" not in g:
        g.db = mysql_conn()
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db:
        db.close()


def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT id, username, email, is_admin FROM users WHERE id=%s", (uid,))
        return cur.fetchone()


def require_login():
    user = current_user()
    if not user:
        abort(403)
    return user


def is_allowed(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image(file_storage):
    if not file_storage or not file_storage.filename:
        return None
    if not is_allowed(file_storage.filename):
        raise ValueError("Bad file type")

    filename = secure_filename(file_storage.filename)
    ext = filename.rsplit(".", 1)[1].lower()
    out_name = f"{uuid4().hex}.{ext}"
    out_path = os.path.join(app.config["UPLOAD_FOLDER"], out_name)

    # Verify image
    img_bytes = file_storage.read()
    img = Image.open(io.BytesIO(img_bytes))  # type: ignore
    img.verify()

    with open(out_path, "wb") as f:
        f.write(img_bytes)

    return out_name


def daily_kjv_verse():
    """
    If verses_kjv table exists, pick a deterministic verse for today.
    If not, show a fallback verse.
    """
    fallback = {"reference": "John 3:16", "text": "For God so loved the world... (KJV)"}

    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("SHOW TABLES LIKE 'verses_kjv'")
            if not cur.fetchone():
                return fallback

            cur.execute("SELECT COUNT(*) AS c FROM verses_kjv")
            total = (cur.fetchone() or {}).get("c", 0)
            if total == 0:
                return fallback

            idx = date.today().toordinal() % total
            cur.execute(
                "SELECT reference, text FROM verses_kjv "
                "ORDER BY (book IS NULL), book, chapter, verse_num, id "
                "LIMIT 1 OFFSET %s",
                (idx,),
            )
            row = cur.fetchone()
            return row or fallback
    except Exception:
        return fallback


@app.before_request
def inject_globals():
    g.user = current_user()
    g.app_title = APP_TITLE
    g.daily_verse = daily_kjv_verse()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/signup", methods=["GET", "POST"])
@limiter.limit("5/minute")
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    username = (request.form.get("username") or "").strip()
    email = (request.form.get("email") or "").strip()
    password = request.form.get("password") or ""

    if not username or not email or len(password) < 8:
        flash("Username, email required, and password must be at least 8 characters.")
        return redirect(url_for("signup"))

    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, email, password_hash, created_at, email_verified, is_admin) "
                "VALUES (%s,%s,%s,%s,0,0)",
                (username, email, generate_password_hash(password), datetime.utcnow()),
            )
        db.commit()
    except IntegrityError:
        db.rollback()
        flash("Username or email already exists.")
        return redirect(url_for("signup"))

    flash("Account created. Please log in.")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
@limiter.limit("10/minute")
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""

    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT id, username, password_hash FROM users WHERE username=%s", (username,))
        u = cur.fetchone()

    if not u or not check_password_hash(u["password_hash"], password):
        flash("Invalid credentials.")
        return redirect(url_for("login"))

    session.clear()
    session["user_id"] = u["id"]
    flash("Welcome back!")
    return redirect(url_for("board"))


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.")
    return redirect(url_for("home"))


@app.route("/board", methods=["GET", "POST"])
@limiter.limit("60/minute")
def board():
    user = require_login()
    db = get_db()

    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        content = (request.form.get("content") or "").strip()
        category = (request.form.get("category") or "").strip()
        is_public = 1  # public board posts are public

        if not title:
            flash("Title is required.")
            return redirect(url_for("board"))

        image_path = None
        file = request.files.get("image")
        if file and file.filename:
            # no image required; keep simple
            if not is_allowed(file.filename):
                flash("Image must be png/jpg/jpeg/gif.")
                return redirect(url_for("board"))
            # Save without Pillow verify if you prefer; we keep it minimal here:
            filename = secure_filename(file.filename)
            ext = filename.rsplit(".", 1)[1].lower()
            out_name = f"{uuid4().hex}.{ext}"
            out_path = os.path.join(app.config["UPLOAD_FOLDER"], out_name)
            file.save(out_path)
            image_path = out_name

        with db.cursor() as cur:
            cur.execute(
                "INSERT INTO prayers (user_id, is_public, title, content, category, image_path, answered, created_at) "
                "VALUES (%s,%s,%s,%s,%s,%s,0,%s)",
                (user["id"], is_public, title, content or None, category or None, image_path, datetime.utcnow()),
            )
        db.commit()
        flash("Prayer posted.")
        return redirect(url_for("board"))

    # Fetch public prayers + replies
    with db.cursor() as cur:
        cur.execute(
            "SELECT p.*, u.username FROM prayers p "
            "JOIN users u ON p.user_id=u.id "
            "WHERE p.is_public=1 AND p.deleted_at IS NULL "
            "ORDER BY p.created_at DESC LIMIT 200"
        )
        prayers = cur.fetchall()

    prayer_ids = [p["id"] for p in prayers]
    comments_map = {pid: [] for pid in prayer_ids}
    if prayer_ids:
        placeholders = ",".join(["%s"] * len(prayer_ids))
        with db.cursor() as cur:
            cur.execute(
                f"SELECT pc.*, u.username FROM prayer_comments pc "
                f"JOIN users u ON pc.user_id=u.id "
                f"WHERE pc.deleted_at IS NULL AND pc.prayer_id IN ({placeholders}) "
                f"ORDER BY pc.created_at ASC",
                prayer_ids,
            )
            for row in cur.fetchall():
                comments_map[row["prayer_id"]].append(row)

    return render_template("board.html", prayers=prayers, comments_map=comments_map)


@app.route("/pray/<int:prayer_id>/reply", methods=["POST"])
@limiter.limit("30/minute")
def reply(prayer_id: int):
    user = require_login()
    content = (request.form.get("content") or "").strip()
    if not content:
        flash("Reply cannot be empty.")
        return redirect(url_for("board"))

    db = get_db()
    with db.cursor() as cur:
        cur.execute(
            "SELECT id FROM prayers WHERE id=%s AND is_public=1 AND deleted_at IS NULL",
            (prayer_id,),
        )
        if not cur.fetchone():
            abort(404)

        cur.execute(
            "INSERT INTO prayer_comments (prayer_id, user_id, content, created_at) VALUES (%s,%s,%s,%s)",
            (prayer_id, user["id"], content, datetime.utcnow()),
        )

    db.commit()
    flash("Reply added.")
    return redirect(url_for("board"))


@app.route("/pray/<int:prayer_id>/toggle-answered")
@limiter.limit("20/minute")
def toggle_answered(prayer_id: int):
    user = require_login()
    db = get_db()
    with db.cursor() as cur:
        cur.execute(
            "SELECT id, answered FROM prayers WHERE id=%s AND deleted_at IS NULL",
            (prayer_id,),
        )
        p = cur.fetchone()
        if not p:
            abort(404)

        new_val = 0 if p["answered"] else 1
        answered_at = datetime.utcnow() if new_val else None
        cur.execute(
            "UPDATE prayers SET answered=%s, answered_at=%s WHERE id=%s",
            (new_val, answered_at, prayer_id),
        )

    db.commit()
    flash("Updated.")
    return redirect(url_for("board"))


@app.route("/admin", methods=["GET"])
def admin():
    user = require_login()
    if not user.get("is_admin"):
        abort(403)

    db = get_db()
    with db.cursor() as cur:
        cur.execute(
            "SELECT p.id, p.title, p.created_at, u.username "
            "FROM prayers p JOIN users u ON p.user_id=u.id "
            "WHERE p.deleted_at IS NULL "
            "ORDER BY p.created_at DESC LIMIT 200"
        )
        prayers = cur.fetchall()

        cur.execute(
            "SELECT pc.id, pc.content, pc.created_at, u.username, pc.prayer_id "
            "FROM prayer_comments pc JOIN users u ON pc.user_id=u.id "
            "WHERE pc.deleted_at IS NULL "
            "ORDER BY pc.created_at DESC LIMIT 200"
        )
        comments = cur.fetchall()

    return render_template("admin.html", prayers=prayers, comments=comments)


@app.route("/admin/prayer/<int:prayer_id>/soft-delete")
def admin_soft_delete_prayer(prayer_id: int):
    user = require_login()
    if not user.get("is_admin"):
        abort(403)
    db = get_db()
    with db.cursor() as cur:
        cur.execute("UPDATE prayers SET deleted_at=NOW() WHERE id=%s AND deleted_at IS NULL", (prayer_id,))
    db.commit()
    flash("Prayer soft-deleted.")
    return redirect(url_for("admin"))


@app.route("/admin/comment/<int:comment_id>/soft-delete")
def admin_soft_delete_comment(comment_id: int):
    user = require_login()
    if not user.get("is_admin"):
        abort(403)
    db = get_db()
    with db.cursor() as cur:
        cur.execute("UPDATE prayer_comments SET deleted_at=NOW() WHERE id=%s AND deleted_at IS NULL", (comment_id,))
    db.commit()
    flash("Comment soft-deleted.")
    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(debug=True)
