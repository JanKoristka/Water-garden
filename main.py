from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, IntegerField, SelectField
from wtforms.validators import DataRequired, InputRequired
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import watering_reminder, get_image


app = Flask(__name__)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my_plants.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
    return render_template("index.html", logged_in=current_user.is_authenticated)


@app.route('/about')
@login_required
def about():
    return render_template("about.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":

        if User.query.filter_by(email=request.form.get('email')).first():
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=request.form.get('email'),
            name=request.form.get('name'),
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("login"))

    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('about'))

    return render_template("login.html", logged_in=current_user.is_authenticated)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = AddPlant()
    try:
        if form.validate_on_submit():
            new_plant = Plant(
                name=form.name.data,
                img_url=get_image(form.name.data),
            )
            db.session.add(new_plant)
            db.session.flush()
            new_info = Watering(
                date_created=form.date.data,
                position=form.position.data,
                water_needs=form.water.data,
                plant_id=new_plant.id,
                user_id=1,
            )
            db.session.add(new_info)
            db.session.commit()
            return redirect(url_for('garden'))
    except KeyError:
        flash("Incorrect name of the plant :-( Be sure that the name of the plant is in correct english latin version!")

    return render_template("add.html", form=form)


@app.route("/edit/", methods=["GET", "POST"])
@login_required
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
@login_required
def delete():
    plant_id = request.args.get('id')
    plant_to_delete = Plant.query.get(plant_id)
    db.session.delete(plant_to_delete)
    db.session.commit()
    # job.remove()
    return redirect(url_for('garden'))

@app.route("/garden")
@login_required
def garden():
    plant = db.session.query(Plant).all()
    watering = db.session.query(Watering).all()
    return render_template("my_garden.html", plants=plant, watering=watering)

@app.route("/photo")
@login_required
def photo():
    plant_id = request.args.get('id')
    plant_to_show = Plant.query.get(plant_id)
    return render_template("show_photo.html", plant=plant_to_show)

# def function():
#     for name in User().query.all():
#         if name.name ==

#schedule.every().day.at("09:00").do(function)
# while True:
#
#     schedule.run_pending()
#     time.sleep(1)


if __name__ == "__main__":
    app.run(debug=True)



