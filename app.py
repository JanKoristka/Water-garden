from datetime import datetime, timedelta
import smtplib
import time
from apscheduler.schedulers.background import BackgroundScheduler

def send_email():
    MY_EMAIL = "********"
    MY_PASSWORD = "********"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject: Your garden needs to be watered! \n\n Your plant is out of water. You should water it."



    )
def watering_reminder(minutes):
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_email,"interval", minutes=minutes)
    scheduler.start()




# def watering_reminder(frequency):
# now = datetime.now().date()
# print(now)


# future = now + timedelta(days=6)
# print(future)
# x = future - now
# print(x)
#     frequency = timedelta(days=[watter_needs])
#     new_watering = plant["date"] + frequency
#     next_water = new_watering + frequency
#     #
#     # next_water = now + timedelta(days=frequency)
#     # if now == next_water:
#     #     send_email()

