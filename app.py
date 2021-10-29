from datetime import datetime, timedelta
import smtplib

def send_email():

    response = smtplib.SMTP()



def watering_reminder(frequency):
    now = datetime.now()
    next_water = now + timedelta(days=frequency)
    if now == next_water:
        send_email()