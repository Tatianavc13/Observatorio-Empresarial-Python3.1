from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash as flasher, jsonify
from flask_login import login_required, current_user
from .. import db
from ..models import Flash

public_bp = Blueprint("public", __name__)
flashes_bp = Blueprint("flashes", __name__, template_folder="../templates/flashes")
api_bp = Blueprint("api", __name__)

# Página pública
@public_bp.route("/")
def home():
    flashes = Flash.query.filter_by(visible=True).order_by(Flash.start_date.asc()).all()
    featured = Flash.query.filter_by(featured=True, visible=True).first()
    return render_template("flashes/list_public.html", flashes=flashes, featured=featured)

@public_bp.route("/flash/<int:flash_id>")
def details(flash_id):
    f = Flash.query.get_or_404(flash_id)
    if not f.visible:
        return redirect(url_for("public.home"))
    return render_template("flashes/detail.html", f=f)

# Admin
@flashes_bp.route("/flashes")
@login_required
def admin_list():
    flashes = Flash.query.order_by(Flash.updated_at.desc()).all()
    return render_template("flashes/list_admin.html", flashes=flashes)

@flashes_bp.route("/flashes/new", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        f = Flash(
            title=request.form["title"],
            description=request.form.get("description"),
            category=request.form.get("category"),
            entity=request.form.get("entity"),
            link=request.form.get("link"),
            location=request.form.get("location"),
            cost=request.form.get("cost"),
            modality=request.form.get("modality"),
        )
        db.session.add(f)
        db.session.commit()
        flasher("Guardado correctamente", "success")
        return redirect(url_for("flashes.admin_list"))
    return render_template("flashes/form.html")

# API JSON
@api_bp.get("/flashes")
def api_list():
    items = Flash.query.filter_by(visible=True).all()
    return jsonify([{
        "id": x.id,
        "title": x.title,
        "category": x.category,
        "entity": x.entity,
        "location": x.location,
        "start_date": x.start_date.isoformat() if x.start_date else None
    } for x in items])
