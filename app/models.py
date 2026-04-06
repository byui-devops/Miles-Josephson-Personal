from app import db


class Car(db.Model):
    __tablename__ = "cars"

    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(64), nullable=False)
    model = db.Column(db.String(128), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    era = db.Column(db.String(16), nullable=False)   # past | present | future
    horsepower = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    forza_available = db.Column(db.Boolean, default=False)
    image_url = db.Column(db.String(512), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "era": self.era,
            "horsepower": self.horsepower,
            "description": self.description,
            "forza_available": self.forza_available,
            "image_url": self.image_url,
        }

    def __repr__(self):
        return f"<Car {self.year} {self.make} {self.model}>"
