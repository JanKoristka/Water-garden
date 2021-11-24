"""Utils module. Containing get_image function that is responsible for displaying the plant image and
watering_reminder and send_email which are both responsible for the BackgroundScheduler working properly."""
import os
from collections import defaultdict
import smtplib
import requests
from datetime import datetime
from water_garden.models import User
from water_garden.extensions import db


def send_email(email, flowers, positions):
    """Send alert email to the user every time his plants need water."""
    MY_EMAIL = os.environ['MY_EMAIL']
    MY_PASSWORD = os.environ['MY_PASSWORD']
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
    """Gets image source of requested house plant from wikipedia.org."""
    request = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"
    PARAMS = {
            "action": "query",
            "format": "json",
            "titles": name,
            "prop": "pageimages",
            "formatversion": 2,
            "pithumbsize": 500,
    }
    response = request.get(url=URL, params=PARAMS)
    data = response.json()
    page_source = data['query']['pages'][0]['thumbnail']['source']
    return page_source


def watering_reminder(app):
    """Checking per user if his plants need to be watered."""
    today = datetime.now().date()
    flower_to_water = {}
    with app.app_context():
        query = db.session.query(User)
        for user in query:
            flower_to_water[user] = defaultdict(list)
            flower_to_water[user]["email"] = user.email
            for plant in user.watering:
                if (today - plant.date_created).days % plant.water_needs == 0:
                    flower_to_water[user]["flower"].append(plant.plant.name)
                    flower_to_water[user]["position"].append(plant.position)
    for user in flower_to_water:
        flowers = flower_to_water[user]["flower"]
        positions = flower_to_water[user]["position"]
        email = flower_to_water[user]["email"]
        send_email(email, flowers, positions)
