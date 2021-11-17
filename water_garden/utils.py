import smtplib
import schedule
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

# def sched_function():
#     flower_to_water = {}
#     for name in User.query.all():
#         flower_to_water[name] = {}
#         flower_to_water[name]["flower"] = []
#         flower_to_water[name]["position"] = []
#         for plant in name.watering:
#             if plant.water_needs == 10:
#                 flower_to_water[name].append()
#
#     for user,flowers in flower_to_water.items():
#         send_email(user,flowers)
#
# # today - date created = number of days % == 0:
#
#
# schedule.every().day.at("09:00").do(sched_function)
# while True:
#
#      schedule.run_pending()
#      time.sleep(1)
