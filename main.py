from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, IntegerField, SelectField
from wtforms.validators import DataRequired
from datetime import datetime
from app import watering_reminder, get_image




app = Flask(__name__)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my_plants.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Plant(db.Model):
    __tablename__ = 'garden'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    date_created = db.Column(db.Date, nullable=False)
    position = db.Column(db.String(250), nullable=False)
    water_needs = db.Column(db.Integer, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f" Plant name is {self.name} and it needs to be water every {self.water_needs} days"

db.create_all()

class AddPlant(FlaskForm):
    name = StringField("Latin name:", validators=[DataRequired()])
    date = DateTimeField("Date:",
                         format="%Y-%m-%d",
                         default=datetime.now().date(),
                         validators=[DataRequired()])
    position = StringField("Position in house:", validators=[DataRequired()])
    water = IntegerField("Water needs every:(days)", validators=[DataRequired()])
    add = SubmitField("Add plant")

class ChangeWater(FlaskForm):
    new_water = IntegerField("New water plan:(days)", validators=[DataRequired()])
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
            water_needs=form.water.data,
            img_url=get_image(form.name.data),
        )
        db.session.add(new_plant)
        db.session.commit()
        #watering_reminder(form.water.data, form.name.data, form.position.data)


        return redirect(url_for('garden'))
    return render_template("add.html", form=form)


@app.route("/edit/", methods=["GET", "POST"])
def edit():
    form = ChangeWater()
    plant_id = request.args.get('id')
    plant = Plant.query.get(plant_id)
    if form.validate_on_submit():
        plant.water_needs = form.new_water.data
        db.session.commit()
        #watering_reminder(form.new_water.data) #form.name.data, form.position.data)
        return redirect(url_for('garden'))

    return render_template("edit.html", form=form, plant=plant)


@app.route("/delete")
def delete():
    plant_id = request.args.get('id')
    plant_to_delete = Plant.query.get(plant_id)
    db.session.delete(plant_to_delete)
    db.session.commit()
    # job.remove()
    return redirect(url_for('garden'))

@app.route("/garden")
def garden():
    all_plants = db.session.query(Plant).all()
    return render_template("my_garden.html", plants=all_plants)

@app.route("/photo")
def photo():
    plant_id = request.args.get('id')
    plant_to_show = Plant.query.get(plant_id)
    return render_template("show_photo.html", plant=plant_to_show)




if __name__ == "__main__":
    app.run(debug=True)



