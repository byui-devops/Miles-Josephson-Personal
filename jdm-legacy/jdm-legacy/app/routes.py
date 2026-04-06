from flask import Blueprint, jsonify, render_template, request, abort
from app.models import Car

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/api/cars", methods=["GET"])
def get_cars():
    era = request.args.get("era")
    forza = request.args.get("forza")

    query = Car.query

    if era and era in ("past", "present", "future"):
        query = query.filter_by(era=era)

    if forza is not None:
        query = query.filter_by(forza_available=(forza.lower() == "true"))

    cars = query.order_by(Car.year).all()
    return jsonify([c.to_dict() for c in cars])


@main.route("/api/cars/<int:car_id>", methods=["GET"])
def get_car(car_id):
    car = Car.query.get_or_404(car_id)
    return jsonify(car.to_dict())


@main.route("/api/cars", methods=["POST"])
def create_car():
    data = request.get_json()
    required = ["make", "model", "year", "era", "horsepower", "description"]
    for field in required:
        if field not in data:
            abort(400, description=f"Missing field: {field}")

    if data["era"] not in ("past", "present", "future"):
        abort(400, description="era must be past, present, or future")

    car = Car(
        make=data["make"],
        model=data["model"],
        year=data["year"],
        era=data["era"],
        horsepower=data["horsepower"],
        description=data["description"],
        forza_available=data.get("forza_available", False),
        image_url=data.get("image_url"),
    )
    from app import db
    db.session.add(car)
    db.session.commit()
    return jsonify(car.to_dict()), 201


@main.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "jdm-legacy"})
