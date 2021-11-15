import smtplib
from apscheduler.schedulers.background import BackgroundScheduler
import requests

import time

def send_email(name, position):
    MY_EMAIL = "xxxxx"
    MY_PASSWORD = "xxxxxx"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject: Your garden needs to be watered! \n\n Your {name} which is positioned in {position} "
                f"is out of water. You should water it."

    )


def watering_reminder(minutes, name, position, id):
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_email,"interval",[name, position],id=id, minutes=minutes, max_instances=100, replace_existing=True)
    scheduler.start()





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

