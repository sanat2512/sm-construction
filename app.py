from unittest import result

from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
import uuid
import pymysql
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name="dzlskdwgd",
    api_key="234567384978218",
    api_secret=os.getenv("CLOUDINARY_SECRET")
)

pymysql.install_as_MySQLdb()

from dotenv import load_dotenv
load_dotenv()
print("HOST:", os.getenv("MYSQL_HOST"))
print("DB:", os.getenv("MYSQL_DB"))
app = Flask(__name__)

# =========================
# SECURITY
# =========================
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "sm_construction_secure_key"
)

app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# enable only on HTTPS hosting
# app.config['SESSION_COOKIE_SECURE'] = True

# upload limit
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024


def login_required(f):

    @wraps(f)
    def wrapper(*args, **kwargs):

        if "admin_id" not in session:
            return redirect("/login")

        return f(*args, **kwargs)

    return wrapper


# =========================
# DB CONFIG
# =========================
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "mysql+pymysql://VszFYNjvEcieXTk.root:M8lYQzas606rnjHX@"
    "gateway01.ap-southeast-1.prod.alicloud.tidbcloud.com:4000/"
    "sm_construction?ssl_verify_cert=false"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True
}

db = SQLAlchemy(app)

# =========================
# UPLOAD CONFIG
# =========================
UPLOAD_FOLDER = os.path.join(
    app.root_path,
    "static",
    "uploads"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

ALLOWED_EXTENSIONS = {
    'png',
    'jpg',
    'jpeg',
    'webp'
}


def allowed_file(filename):

    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# =========================
# MODELS
# =========================
class Service(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    image = db.Column(
        db.String(200)
    )


class Project(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200)
    )

    description = db.Column(
        db.Text
    )

    image = db.Column(
        db.String(300)
    )

    location = db.Column(
        db.String(200)
    )

    completion_year = db.Column(
        db.String(50)
    )

    client = db.Column(
        db.String(200)
    )

    service_id = db.Column(
        db.Integer,
        db.ForeignKey('service.id')
    )

    service = db.relationship(
        'Service',
        backref='projects'
    )


class ProjectImage(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    image = db.Column(
        db.String(300)
    )

    project_id = db.Column(
        db.Integer,
        db.ForeignKey('project.id')
    )


class Contact(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(200)
    )

    phone = db.Column(
        db.String(50)
    )

    message = db.Column(
        db.Text
    )

    is_read = db.Column(
        db.Boolean,
        default=False
    )


class Admin(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        unique=True
    )

    password = db.Column(
        db.String(200)
    )


# =========================
# HOME
# =========================
@app.route("/")
def home():

    projects = Project.query.all()

    services = Service.query.all()

    return render_template(
        "index.html",
        projects=projects,
        services=services
    )


# =========================
# SERVICE PAGE
# =========================
@app.route("/service/<int:id>")
def service_page(id):

    service = Service.query.get_or_404(id)

    projects = Project.query.filter_by(
        service_id=id
    ).all()

    return render_template(
        "service.html",
        service=service,
        projects=projects
    )


# =========================
# PROJECT DETAIL
# =========================
@app.route("/project/<int:id>")
def project_detail(id):

    project = Project.query.get_or_404(id)

    gallery = ProjectImage.query.filter_by(
        project_id=id
    ).all()

    return render_template(
        "project_detail.html",
        project=project,
        gallery=gallery
    )


# =========================
# CONTACT FORM
# =========================
@app.route(
    "/contact",
    methods=["POST"]
)
def contact():

    name = request.form.get("name")

    phone = request.form.get("phone")

    message = request.form.get("message")

    if not name or not phone or not message:

        return redirect("/#contact")

    new_contact = Contact(
        name=name,
        phone=phone,
        message=message
    )

    db.session.add(new_contact)

    db.session.commit()

    return redirect("/#contact")


# =========================
# LOGIN
# =========================
@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    error = None

    if request.method == "POST":

        username = request.form.get(
            "username"
        )

        password = request.form.get(
            "password"
        )

        admin = Admin.query.filter_by(
            username=username
        ).first()

        if admin and check_password_hash(
            admin.password,
            password
        ):

            session["admin_id"] = admin.id

            return redirect("/admin")

        error = "Invalid login"

    return render_template(
        "login.html",
        error=error
    )


# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# =========================
# ADMIN
# =========================
@app.route(
    "/admin",
    methods=["GET", "POST"]
)
@login_required
def admin():

    if request.method == "POST":

        image = request.files.get("image")

        if image and allowed_file(image.filename):

            # upload main image to cloudinary
            result = cloudinary.uploader.upload(image)
            image_url = result["secure_url"]

            project = Project(
                title=request.form.get("title"),
                description=request.form.get("description"),
                image=image_url,
                location=request.form.get("location"),
                completion_year=request.form.get("completion_year"),
                client=request.form.get("client"),
                service_id=request.form.get("service_id")
            )

            db.session.add(project)
            db.session.commit()

            # =========================
            # GALLERY IMAGES
            # =========================
            gallery_files = request.files.getlist("gallery_images")

            for file in gallery_files:
                if file and allowed_file(file.filename):

                    result = cloudinary.uploader.upload(file)
                    gname = result["secure_url"]

                    db.session.add(
                        ProjectImage(
                            image=gname,
                            project_id=project.id
                        )
                    )

            db.session.commit()

    total_msgs = Contact.query.count()
    unread_msgs = Contact.query.filter_by(is_read=False).count()
    read_msgs = Contact.query.filter_by(is_read=True).count()

    project_images = {}

    for p in Project.query.all():
        project_images[p.id] = ProjectImage.query.filter_by(
            project_id=p.id
        ).all()

    return render_template(
        "admin.html",
        projects=Project.query.all(),
        services=Service.query.all(),
        contacts=Contact.query.all(),
        total_msgs=total_msgs,
        unread_msgs=unread_msgs,
        read_msgs=read_msgs,
        project_images=project_images
    )

# =========================
# ADD SERVICE
# =========================
@app.route("/add-service", methods=["POST"])
@login_required
def add_service():

    image = request.files.get("image")

    if image and allowed_file(image.filename):

        result = cloudinary.uploader.upload(image)
        image_url = result["secure_url"]

        service = Service(
            name=request.form.get("name"),
            description=request.form.get("description"),
            image=image_url
        )

        db.session.add(service)
        db.session.commit()

    return redirect("/admin")

@app.route("/edit-service/<int:id>", methods=["GET", "POST"])
@login_required
def edit_service(id):

    service = Service.query.get_or_404(id)

    if request.method == "POST":

        service.name = request.form.get("name")
        service.description = request.form.get("description")

        image = request.files.get("image")

        if image and allowed_file(image.filename):

            result = cloudinary.uploader.upload(image)
            service.image = result["secure_url"]

        db.session.commit()
        return redirect("/admin")

    return render_template("edit_service.html", service=service)
# =========================
# DELETE SERVICE
# =========================
@app.route(
    "/delete-service/<int:id>",
    methods=["POST"]
)
@login_required
def delete_service(id):

    service = Service.query.get_or_404(id)

    if service.image:

        path = os.path.join(
            UPLOAD_FOLDER,
            service.image
        )

        if os.path.exists(path):

            os.remove(path)

    for p in service.projects:

        p.service_id = None

    db.session.delete(service)

    db.session.commit()

    return redirect("/admin")


# =========================
# EDIT PROJECT
# =========================
@app.route(
    "/edit-project/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit_project(id):

    project = Project.query.get_or_404(id)

    if request.method == "POST":

        project.title = request.form.get(
            "title"
        )

        project.description = request.form.get(
            "description"
        )

        project.location = request.form.get(
            "location"
        )

        project.completion_year = request.form.get(
            "completion_year"
        )

        project.client = request.form.get(
            "client"
        )

        project.service_id = request.form.get(
            "service_id"
        )

        image = request.files.get("image")

        if image and allowed_file(
            image.filename
        ):

            if project.image:

                old_path = os.path.join(
                    UPLOAD_FOLDER,
                    project.image
                )

                if os.path.exists(
                    old_path
                ):

                    os.remove(old_path)

        if image and allowed_file(image.filename):

           result = cloudinary.uploader.upload(image)
           project.image = result["secure_url"]

        db.session.commit()

        return redirect("/admin")

    return render_template(
        "edit_project.html",
        project=project,
        services=Service.query.all()
    )


# =========================
# DELETE PROJECT
# =========================
@app.route(
    "/delete/<int:id>",
    methods=["POST"]
)
@login_required
def delete_project(id):

    project = Project.query.get_or_404(id)

    if project.image:

        path = os.path.join(
            UPLOAD_FOLDER,
            project.image
        )

        if os.path.exists(path):

            os.remove(path)

    gallery = ProjectImage.query.filter_by(
        project_id=id
    ).all()

    for g in gallery:

        gpath = os.path.join(
            UPLOAD_FOLDER,
            g.image
        )

        if os.path.exists(gpath):

            os.remove(gpath)

        db.session.delete(g)

    db.session.delete(project)

    db.session.commit()

    return redirect("/admin")


# =========================
# DELETE GALLERY IMAGE
# =========================
@app.route(
    "/delete-gallery-image/<int:id>",
    methods=["POST"]
)
@login_required
def delete_gallery_image(id):

    image = ProjectImage.query.get_or_404(id)

    path = os.path.join(
        UPLOAD_FOLDER,
        image.image
    )

    if os.path.exists(path):

        os.remove(path)

    db.session.delete(image)

    db.session.commit()

    return redirect("/admin")


# =========================
# MARK MESSAGE AS READ
# =========================
@app.route(
    "/mark-read/<int:id>",
    methods=["POST"]
)
@login_required
def mark_read(id):

    msg = Contact.query.get_or_404(id)

    msg.is_read = True

    db.session.commit()

    return redirect("/admin#messages")


# =========================
# DELETE MESSAGE
# =========================
@app.route(
    "/delete-message/<int:id>",
    methods=["POST"]
)
@login_required
def delete_message(id):

    msg = Contact.query.get_or_404(id)

    db.session.delete(msg)

    db.session.commit()

    return redirect("/admin#messages")


# =========================
# CHANGE PASSWORD
# =========================
@app.route(
    "/change-password",
    methods=["GET", "POST"]
)
@login_required
def change_password():

    message = None

    admin = Admin.query.get(
        session["admin_id"]
    )

    if request.method == "POST":

        current = request.form.get(
            "current_password"
        )

        new = request.form.get(
            "new_password"
        )

        confirm = request.form.get(
            "confirm_password"
        )

        if not check_password_hash(
            admin.password,
            current
        ):

            message = (
                "Wrong current password"
            )

        elif new != confirm:

            message = (
                "Passwords do not match"
            )

        elif len(new) < 5:

            message = (
                "Password too short"
            )

        else:

            admin.password = (
                generate_password_hash(
                    new
                )
            )

            db.session.commit()

            message = (
                "Password updated successfully"
            )

    return render_template(
        "change_password.html",
        message=message
    )


# =========================
# INIT DB
# =========================
with app.app_context():

    try:

        db.create_all()

    except Exception as e:

        print("DB ERROR:", e)

    if not Admin.query.filter_by(
        username="admin"
    ).first():

        db.session.add(
            Admin(
                username="admin",
                password=generate_password_hash(
                    "Admin@123"
                )
            )
        )

        db.session.commit()


# =========================
# RUN
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(
            os.environ.get(
                "PORT",
                10000
            )
        ),
        debug=False
    )
