"""Forms module. Containing two classes - flask forms - AddPlant and ChangeWater."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, IntegerField
from wtforms.validators import DataRequired
from datetime import datetime


class AddPlant(FlaskForm):
    """Form for adding new plant to the garden."""
    name = StringField("Latin name:", validators=[DataRequired()])
    date = DateTimeField("Date:",
                         format="%Y-%m-%d",
                         default=datetime.now().date(),
                         validators=[DataRequired()])
    position = StringField("Place in your house:", validators=[DataRequired()])
    water = IntegerField("Water needs every:(days)", validators=[DataRequired()])
    add = SubmitField("Add plant")


class ChangeWater(FlaskForm):
    """Form for editing water needs of plant in user garden."""
    new_water = IntegerField("New water plan:(days)", validators=[DataRequired()])
    change = SubmitField("Change")