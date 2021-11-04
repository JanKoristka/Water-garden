import smtplib
from apscheduler.schedulers.background import BackgroundScheduler


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

