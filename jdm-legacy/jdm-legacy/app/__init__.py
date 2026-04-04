from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app(config=None):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL",
        "postgresql://jdmuser:jdmpass@localhost:5432/jdmlegacy"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if config:
        app.config.update(config)

    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()
        _seed_data()

    return app


def _seed_data():
    from app.models import Car
    if Car.query.count() == 0:
        cars = [
            # PAST
            Car(make="Nissan", model="Skyline GT-R R32", year=1989, era="past",
                horsepower=280, description="The legendary Godzilla. All-wheel drive, twin-turbo RB26DETT inline-six. Dominated Group A racing worldwide.",
                forza_available=True, image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Nissan_Skyline_GT-R_%28R32%29_001.jpg/1280px-Nissan_Skyline_GT-R_%28R32%29_001.jpg"),
            Car(make="Toyota", model="Supra MK4", year=1993, era="past",
                horsepower=320, description="The 2JZ-GTE engine is the stuff of legend. Overbuilt from the factory and capable of 1000+ hp with minimal mods.",
                forza_available=True, image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/1997_Toyota_Supra_RZ.jpg/1280px-1997_Toyota_Supra_RZ.jpg"),
            Car(make="Honda", model="NSX", year=1990, era="past",
                horsepower=270, description="Ayrton Senna helped develop this mid-engine masterpiece. Redefined what a supercar could feel like to drive daily.",
                forza_available=True, image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Honda-NSX-NA1.jpg/1280px-Honda-NSX-NA1.jpg"),
            Car(make="Mazda", model="RX-7 FD", year=1992, era="past",
                horsepower=255, description="Twin-turbo rotary perfection. Lightweight, balanced, and unlike anything else on the road.",
                forza_available=True, image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/97_Mazda_RX7.jpg/1280px-97_Mazda_RX7.jpg"),
            Car(make="Mitsubishi", model="Lancer Evolution VI", year=1999, era="past",
                horsepower=280, description="The Tommi Makinen Edition. Rally-bred AWD monster that terrorized WRC stages worldwide.",
                forza_available=True, image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Mitsubishi_Lancer_Evolution_VI_TME.jpg/1280px-Mitsubishi_Lancer_Evolution_VI_TME.jpg"),
            # PRESENT
            Car(make="Toyota", model="GR Yaris", year=2020, era="present",
                horsepower=268, description="A homologation special built around WRC. All-wheel drive, 1.6L three-cylinder turbo in a tiny hot hatch body.",
                forza_available=True, image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/2020_Toyota_GR_Yaris_%281%29.jpg/1280px-2020_Toyota_GR_Yaris_%281%29.jpg"),
            Car(make="Nissan", model="GT-R NISMO", year=2023, era="present",
                horsepower=600, description="The latest evolution of Godzilla. Track-tuned, twin-turbo V6, and still terrifying on the Nürburgring.",
                forza_available=True, image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Nissan_GT-R_NISMO_%28R35%29.jpg/1280px-Nissan_GT-R_NISMO_%28R35%29.jpg"),
            Car(make="Honda", model="Civic Type R FL5", year=2023, era="present",
                horsepower=315, description="The most powerful Type R ever. Front-wheel drive perfection that embarrasses far more expensive cars on track.",
                forza_available=True, image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/2023_Honda_Civic_Type_R_%28FL5%29.jpg/1280px-2023_Honda_Civic_Type_R_%28FL5%29.jpg"),
            Car(make="Subaru", model="BRZ tS", year=2022, era="present",
                horsepower=228, description="Pure driving pleasure. Naturally aspirated, rear-wheel drive, and tuned by STI for sharper dynamics.",
                forza_available=True, image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/2022_Subaru_BRZ_tS_%281%29.jpg/1280px-2022_Subaru_BRZ_tS_%281%29.jpg"),
            Car(make="Lexus", model="LFA", year=2012, era="present",
                horsepower=553, description="A 4.8L V10 that spins to 9000 RPM. Built with carbon fiber and the soul of a race car. Only 500 made.",
                forza_available=True, image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Lexus_LFA_001.jpg/1280px-Lexus_LFA_001.jpg"),
            # FUTURE
            Car(make="Toyota", model="GR GT3 Concept", year=2026, era="future",
                horsepower=500, description="Toyota's vision for a road-legal GT3 racer. Expected to feature hybrid AWD and advanced aerodynamics.",
                forza_available=False, image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Toyota_GR_GT3_Concept.jpg/1280px-Toyota_GR_GT3_Concept.jpg"),
            Car(make="Nissan", model="Hyper Force Concept", year=2025, era="future",
                horsepower=1000, description="1000 horsepower EV/hybrid concept previewing the next GT-R. Shown at Japan Mobility Show 2023.",
                forza_available=False, image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Nissan_Hyper_Force_Concept_%282023%29.jpg/1280px-Nissan_Hyper_Force_Concept_%282023%29.jpg"),
            Car(make="Honda", model="Prelude Concept", year=2025, era="future",
                horsepower=200, description="A revival of the iconic Prelude nameplate as a hybrid sport coupe. Confirmed for limited production.",
                forza_available=False, image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/2024_Honda_Prelude_Concept.jpg/1280px-2024_Honda_Prelude_Concept.jpg"),
            Car(make="Mazda", model="Iconic SP Concept", year=2026, era="future",
                horsepower=370, description="Rotary-hybrid revival concept. A spiritual successor to the RX-7 with a two-rotor hybrid powertrain.",
                forza_available=False, image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Mazda_Iconic_SP.jpg/1280px-Mazda_Iconic_SP.jpg"),
        ]
        db.session.add_all(cars)
        db.session.commit()
