from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash as flasher, jsonify, make_response
from flask_login import login_required, current_user
from .. import db
from ..models import Flash, Company
from sqlalchemy.exc import SQLAlchemyError

public_bp = Blueprint("public", __name__)
flashes_bp = Blueprint("flashes", __name__, template_folder="../templates/flashes")
api_bp = Blueprint("api", __name__)

# Página pública
@public_bp.route("/")
def home():
    flashes = Flash.query.filter_by(visible=True).order_by(Flash.start_date.asc()).all()
    featured = Flash.query.filter_by(featured=True, visible=True).first()

    # Company info (take first or None)
    company = Company.query.first()

    # Category counts
    from sqlalchemy import func
    counts = (
        db.session.query(Flash.category, func.count(Flash.id))
        .filter(Flash.visible == True)
        .group_by(Flash.category)
        .all()
    )
    category_counts = { (c or 'Sin categoría'): n for c, n in counts }

    # Monthly series (count by month for last 12 months)
    # Works with SQLite: use strftime, otherwise fallback
    try:
        monthly_rows = (
            db.session.query(func.strftime('%Y-%m', Flash.start_date), func.count(Flash.id))
            .filter(Flash.visible == True, Flash.start_date.isnot(None))
            .group_by(func.strftime('%Y-%m', Flash.start_date))
            .order_by(func.strftime('%Y-%m', Flash.start_date))
            .all()
        )
        # Convertir Rows a tuplas serializables
        monthly = [(str(r[0]) if r[0] is not None else None, int(r[1])) for r in monthly_rows]
    except Exception:
        monthly = []

    return render_template(
        "flashes/list_public.html",
        flashes=flashes,
        featured=featured,
        company=company,
        category_counts=category_counts,
        monthly=monthly,
    )

@public_bp.route("/flash/<int:flash_id>")
def details(flash_id):
    f = Flash.query.get_or_404(flash_id)
    if not f.visible:
        return redirect(url_for("public.home"))
    return render_template("flashes/detail.html", f=f)

# Página imprimible con portada y pie de página
@public_bp.route("/flash/<int:flash_id>/print")
def print_flash(flash_id):
    f = Flash.query.get_or_404(flash_id)
    company = Company.query.first()
    html = render_template("flashes/print.html", f=f, company=company)
    response = make_response(html)
    response.headers["Content-Type"] = "text/html; charset=utf-8"
    return response

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
        def parse_date(name):
            value = (request.form.get(name) or "").strip()
            try:
                return date.fromisoformat(value) if value else None
            except ValueError:
                return None

        visible = True if request.form.get("visible") == "on" else False
        featured = True if request.form.get("featured") == "on" else False

        try:
            f = Flash(
                title=request.form["title"].strip(),
                description=request.form.get("description"),
                category=request.form.get("category"),
                entity=request.form.get("entity"),
                link=(request.form.get("link") or None),
                location=request.form.get("location"),
                cost=request.form.get("cost"),
                modality=request.form.get("modality"),
                schedule=request.form.get("schedule"),
                start_date=parse_date("start_date"),
                end_date=parse_date("end_date"),
                deadline=parse_date("deadline"),
                visible=visible,
                featured=featured,
            )
            db.session.add(f)
            db.session.commit()
            flasher("Guardado correctamente", "success")
            return redirect(url_for("flashes.admin_list"))
        except (KeyError, SQLAlchemyError):
            db.session.rollback()
            flasher("Error al guardar. Revisa los campos obligatorios.", "danger")
    return render_template("flashes/form.html")

@flashes_bp.route("/flashes/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit(id):
    f = Flash.query.get_or_404(id)
    
    if request.method == "POST":
        def parse_date(name):
            value = (request.form.get(name) or "").strip()
            try:
                return date.fromisoformat(value) if value else None
            except ValueError:
                return None

        visible = True if request.form.get("visible") == "on" else False
        featured = True if request.form.get("featured") == "on" else False

        try:
            f.title = request.form["title"].strip()
            f.description = request.form.get("description")
            f.category = request.form.get("category")
            f.entity = request.form.get("entity")
            f.link = (request.form.get("link") or None)
            f.location = request.form.get("location")
            f.cost = request.form.get("cost")
            f.modality = request.form.get("modality")
            f.schedule = request.form.get("schedule")
            f.start_date = parse_date("start_date")
            f.end_date = parse_date("end_date")
            f.deadline = parse_date("deadline")
            f.visible = visible
            f.featured = featured
            
            db.session.commit()
            flasher("Actualizado correctamente", "success")
            return redirect(url_for("flashes.admin_list"))
        except (KeyError, SQLAlchemyError):
            db.session.rollback()
            flasher("Error al actualizar. Revisa los campos obligatorios.", "danger")
    
    return render_template("flashes/form.html", flash=f)

@flashes_bp.route("/flashes/<int:id>/toggle-visibility", methods=["POST"])
@login_required
def toggle_visibility(id):
    f = Flash.query.get_or_404(id)
    try:
        f.visible = not f.visible
        db.session.commit()
        return jsonify({"success": True, "visible": f.visible})
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"success": False}), 500

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
