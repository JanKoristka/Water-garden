from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my_plants.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CREATE TABLE

class Plant(db.Model):
    __tablename__ = 'garden'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    date_created = db.Column(db.Integer, nullable=False)
    position = db.Column(db.String(250), nullable=False)
    water_needs = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f" Plant name is {self.name} and it needs to be water every {self.water_needs} days"

db.create_all()

class AddPlant(FlaskForm):
    name = StringField("Plant name:", validators=[DataRequired()])
    date = StringField("Date:", validators=[DataRequired()])
    position = StringField("Position:", validators=[DataRequired()])
    water = StringField("Water needs every:(days)", validators=[DataRequired()])
    add = SubmitField("Add plant")

class ChangeWater(FlaskForm):
    new_water = StringField("New water plan:(days)", validators=[DataRequired()])
    change = SubmitField("Change")



@app.route('/')
def home():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddPlant()
    if form.validate_on_submit():
        new_plant = Plant(
            name=form.name.data,
            date_created=form.date.data,
            position=form.position.data,
            water_needs=form.water.data
        )
        db.session.add(new_plant)
        db.session.commit()
        return redirect(url_for('garden'))

    return render_template("add.html", form=form)


@app.route("/edit/", methods=["GET", "POST"])
def edit():
    form = ChangeWater()
    plant_id = request.args.get('id')
    update_plant = Plant.query.get(plant_id)
    if form.validate_on_submit():
        update_plant.water_needs = form.new_water.data
        db.session.commit()
        return redirect(url_for('garden'))

    return render_template("edit.html", form=form)


@app.route("/delete")
def delete():
    plant_id = request.args.get('id')
    plant_to_delete = Plant.query.get(plant_id)
    db.session.delete(plant_to_delete)
    db.session.commit()
    return redirect(url_for('garden'))

@app.route("/garden")
def garden():
    all_plants = db.session.query(Plant).all()
    return render_template("my_garden.html", plants=all_plants)

if __name__ == "__main__":
    app.run(debug=True)



