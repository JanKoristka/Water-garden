import smtplib
import requests
from datetime import datetime
from water_garden.models import User, Plant
from water_garden.extensions import db


def send_email(email, flowers, positions):
    MY_EMAIL = "xxxxxxx"
    MY_PASSWORD = "xxxxxxx"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        msg = ""
        for flower, position in zip(flowers, positions):
            msg += f"flower {flower} positioned on {position}\n"
            final_msg = f"Subject: Your garden needs to be watered! \n\n {msg}"
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=email,
            msg=final_msg
    )

def get_image(name):
    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"
    PARAMS = {
            "action": "query",
            "format": "json",
            "titles": name,
            "prop": "pageimages",
            "formatversion": 2,
            "pithumbsize": 500,
    }
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    page_source = DATA['query']['pages'][0]['thumbnail']['source']
    return page_source

def watering_reminder(app):
    today = datetime.now().date()
    flower_to_water = {}
    with app.app_context():
        query = db.session.query(User)
        for user in query:
            flower_to_water[user] = {}
            flower_to_water[user]["email"] = user.email
            flower_to_water[user]["flower"] = []
            flower_to_water[user]["position"] = []
            for plant in user.watering:
                if (today - plant.date_created).days % plant.water_needs == 0:
                    flower_to_water[user]["flower"].append(plant.plant.name)
                    flower_to_water[user]["position"].append(plant.position)
    for user in flower_to_water:
        flowers = flower_to_water[user]["flower"]
        positions = flower_to_water[user]["position"]
        email = flower_to_water[user]["email"]
        send_email(email, flowers, positions)
