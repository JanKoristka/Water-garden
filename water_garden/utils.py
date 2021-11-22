import smtplib
import requests
from datetime import datetime
from water_garden.models import User
from water_garden.extensions import db


def send_email(flowers, positions):
    MY_EMAIL = "xxxxxx"
    MY_PASSWORD = "xxxxx"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        msq = ""
        for flower, position in zip(flowers, positions):
            msq += f"flower {flower} positioned on {position}"
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject: Your garden needs to be watered! \n\n {msg}"


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
            flower_to_water[user]["flower"] = []
            flower_to_water[user]["position"] = []
            for plant in user.watering:
                if (today - plant.date_created).days % plant.water_needs == 0:
                    flower_to_water[user]["flower"].append(plant.plant_id)
                    flower_to_water[user]["position"].append(plant.position)
    for flowers,position in flower_to_water.items():
        print(flowers, position)
