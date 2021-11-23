"""Models module. Containing three classes - db tables - User, Plant, Watering."""
from flask_login import UserMixin
from water_garden.extensions import db


class User(UserMixin, db.Model):
    """Table for user information."""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    watering = db.relationship("Watering", back_populates="user")


class Plant(db.Model):
    """Table for unique plant names and images."""
    __tablename__ = 'plant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    watering = db.relationship("Watering", back_populates="plant")


class Watering(db.Model):
    """Table for watering info."""
    __tablename__ = 'watering'
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.Date, nullable=False)
    position = db.Column(db.String(250), nullable=False)
    water_needs = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"), nullable=False)
    plant_id = db.Column(db.Integer,db.ForeignKey("plant.id"), nullable=False)
    plant = db.relationship("Plant", back_populates="watering")
    user = db.relationship("User", back_populates="watering")

