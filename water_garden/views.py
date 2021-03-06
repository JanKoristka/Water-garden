"""Views module. This is where the routes are defined."""
from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from water_garden.models import User, Plant, Watering
from water_garden.forms import AddPlant, ChangeWater
from water_garden.utils import get_image
from water_garden.extensions import db, login_manager
from water_garden.logger import logger


blueprint = Blueprint("views", __name__, static_folder="/static", template_folder='/templates')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@blueprint.route('/')
def home():
    logger.info("Processing default request")
    return render_template("index.html", logged_in=current_user.is_authenticated)


@blueprint.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":

        if User.query.filter_by(email=request.form.get('email')).first():
            logger.warning("User is already registered")
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('views.login'))

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
        logger.info("New user has been registered")
        return redirect(url_for("views.login"))

    return render_template("register.html", logged_in=current_user.is_authenticated)


@blueprint.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if not user:
            logger.warning("User email does not exist")
            flash("That email does not exist, please try again.")
            return redirect(url_for('views.login'))
        elif not check_password_hash(user.password, password):
            logger.warning("User inputted incorrect password")
            flash('Password incorrect, please try again.')
            return redirect(url_for('views.login'))
        else:
            login_user(user)
            logger.info(f"{current_user.email} successfully logged in.")
            return redirect(url_for('views.about'))

    return render_template("login.html", logged_in=current_user.is_authenticated)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    logger.info("User logged of.")
    return redirect(url_for('views.home'))


@blueprint.route('/about')
@login_required
def about():
    logger.info(f"{current_user.email} is reading about app")
    return render_template("about.html")


@blueprint.route("/garden")
@login_required
def garden():
    plant = db.session.query(Watering.position, Watering.water_needs, Plant.name, Plant.id).join(Plant,
    Plant.id == Watering.plant_id).join(User, User.id == Watering.user_id).filter(Watering.user_id == current_user.id)
    return render_template("my_garden.html", plants=plant)


@blueprint.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = AddPlant()
    try:
        if form.validate_on_submit():
            new_plant = Plant.query.filter_by(name=form.name.data).first()
            if new_plant is None:
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
                user_id=current_user.id,
            )
            db.session.add(new_info)
            db.session.commit()
            logger.info(f"{current_user.email} added new plant to his garden")
            return redirect(url_for('views.garden'))
    except KeyError:
        logger.warning(f"{current_user.email} inputted incorrect name of the plant")
        flash("Incorrect name of the plant :-( Be sure that the name of the plant is in correct latin version!")
    return render_template("add.html", form=form)


@blueprint.route("/edit/", methods=["GET", "POST"])
@login_required
def edit():
    form = ChangeWater()
    water_id = request.args.get('id')
    plant = Watering.query.filter(Watering.id == water_id).first()
    if form.validate_on_submit():
        plant.water_needs = form.new_water.data
        db.session.commit()
        logger.warning(f"{current_user.email} changed water needs of the plant")
        return redirect(url_for('views.garden'))

    return render_template("edit.html", form=form, plant=plant)


@blueprint.route("/delete")
@login_required
def delete():
    plant_id = request.args.get('id')
    Watering.query.filter(Watering.user_id == current_user.id).filter(Watering.plant_id == plant_id).delete()
    db.session.commit()
    logger.warning(f"{current_user.email} deleted plant from his garden")
    return redirect(url_for('views.garden'))


@blueprint.route("/photo")
@login_required
def photo():
    plant_id = request.args.get('id')
    plant_to_show = Plant.query.get(plant_id)
    logger.info(f"{current_user.email} viewed plant photo")
    return render_template("show_photo.html", plant=plant_to_show)

