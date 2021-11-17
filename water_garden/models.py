from flask_login import UserMixin
from water_garden.extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    watering = db.relationship("Watering")


class Plant(db.Model):
    __tablename__ = 'plant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    watering = db.relationship("Watering")

class Watering(db.Model):
    __tablename__ = 'watering'
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.Date, nullable=False)
    position = db.Column(db.String(250), nullable=False)
    water_needs = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"), nullable=False)
    plant_id = db.Column(db.Integer,db.ForeignKey("plant.id"), nullable=False)
