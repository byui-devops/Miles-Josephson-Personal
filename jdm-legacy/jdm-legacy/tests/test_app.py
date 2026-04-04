"""
JDM Legacy — Test Suite
Unit tests: Car model logic
Integration tests: API routes via Flask test client + SQLite in-memory DB
"""
import pytest
from app import create_app, db
from app.models import Car


# ── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def app():
    """Create application with in-memory SQLite for testing."""
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    }
    application = create_app(config=test_config)
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def sample_car(app):
    with app.app_context():
        car = Car(
            make="Nissan",
            model="Skyline GT-R R32",
            year=1989,
            era="past",
            horsepower=280,
            description="The legendary Godzilla.",
            forza_available=True,
            image_url="https://example.com/r32.jpg",
        )
        db.session.add(car)
        db.session.commit()
        return car.id  # return ID so we can re-query inside other app contexts


# ── UNIT TESTS: Car model ────────────────────────────────────────────────────

class TestCarModel:

    def test_car_repr(self, app, sample_car):
        with app.app_context():
            car = Car.query.get(sample_car)
            assert "Nissan" in repr(car)
            assert "R32" in repr(car)

    def test_car_to_dict_keys(self, app, sample_car):
        with app.app_context():
            car = Car.query.get(sample_car)
            d = car.to_dict()
            for key in ["id", "make", "model", "year", "era", "horsepower", "description", "forza_available", "image_url"]:
                assert key in d

    def test_car_to_dict_values(self, app, sample_car):
        with app.app_context():
            car = Car.query.get(sample_car)
            d = car.to_dict()
            assert d["make"] == "Nissan"
            assert d["year"] == 1989
            assert d["era"] == "past"
            assert d["horsepower"] == 280
            assert d["forza_available"] is True

    def test_car_default_forza_false(self, app):
        with app.app_context():
            car = Car(make="Honda", model="Prelude", year=2025, era="future",
                      horsepower=200, description="Concept car.")
            db.session.add(car)
            db.session.commit()
            assert car.forza_available is False

    def test_car_era_values(self, app):
        with app.app_context():
            for era in ("past", "present", "future"):
                car = Car(make="Toyota", model=f"Test {era}", year=2000,
                          era=era, horsepower=200, description="Test.")
                db.session.add(car)
            db.session.commit()
            assert Car.query.filter_by(era="past").count() >= 1
            assert Car.query.filter_by(era="present").count() >= 1
            assert Car.query.filter_by(era="future").count() >= 1


# ── INTEGRATION TESTS: API routes ────────────────────────────────────────────

class TestHealthEndpoint:

    def test_health_returns_200(self, client):
        res = client.get("/api/health")
        assert res.status_code == 200

    def test_health_json(self, client):
        res = client.get("/api/health")
        data = res.get_json()
        assert data["status"] == "ok"
        assert data["service"] == "jdm-legacy"


class TestGetCars:

    def test_get_all_cars_empty(self, client):
        res = client.get("/api/cars")
        assert res.status_code == 200
        # May have seeded data — check it's a list
        assert isinstance(res.get_json(), list)

    def test_get_cars_era_filter(self, app, client, sample_car):
        res = client.get("/api/cars?era=past")
        assert res.status_code == 200
        cars = res.get_json()
        for c in cars:
            assert c["era"] == "past"

    def test_get_cars_forza_filter_true(self, client):
        res = client.get("/api/cars?forza=true")
        assert res.status_code == 200
        cars = res.get_json()
        for c in cars:
            assert c["forza_available"] is True

    def test_get_cars_forza_filter_false(self, client):
        res = client.get("/api/cars?forza=false")
        assert res.status_code == 200
        cars = res.get_json()
        for c in cars:
            assert c["forza_available"] is False

    def test_invalid_era_returns_all(self, client):
        res = client.get("/api/cars?era=invalid")
        assert res.status_code == 200


class TestGetSingleCar:

    def test_get_car_by_id(self, app, client, sample_car):
        res = client.get(f"/api/cars/{sample_car}")
        assert res.status_code == 200
        data = res.get_json()
        assert data["make"] == "Nissan"
        assert data["model"] == "Skyline GT-R R32"

    def test_get_car_not_found(self, client):
        res = client.get("/api/cars/99999")
        assert res.status_code == 404


class TestCreateCar:

    def test_create_car_success(self, client):
        payload = {
            "make": "Mazda",
            "model": "RX-7 FD",
            "year": 1992,
            "era": "past",
            "horsepower": 255,
            "description": "Twin-turbo rotary perfection.",
            "forza_available": True,
        }
        res = client.post("/api/cars", json=payload)
        assert res.status_code == 201
        data = res.get_json()
        assert data["make"] == "Mazda"
        assert data["id"] is not None

    def test_create_car_missing_field(self, client):
        payload = {"make": "Toyota", "model": "Supra"}  # missing required fields
        res = client.post("/api/cars", json=payload)
        assert res.status_code == 400

    def test_create_car_invalid_era(self, client):
        payload = {
            "make": "Subaru",
            "model": "Impreza",
            "year": 2000,
            "era": "ancient",  # invalid
            "horsepower": 250,
            "description": "Rally car.",
        }
        res = client.post("/api/cars", json=payload)
        assert res.status_code == 400


class TestIndexRoute:

    def test_index_returns_200(self, client):
        res = client.get("/")
        assert res.status_code == 200
        assert b"JDM Legacy" in res.data
