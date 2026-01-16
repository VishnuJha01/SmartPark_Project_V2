from celery import shared_task
import csv
import datetime
import requests
from jinja2 import Template
from .model import User, Reservation
from .mails import send_email


@shared_task(ignore_results=False, name="export_csv")
def export_csv(user_id):
    user = User.query.get(user_id)
    if not user:
        return "User not found."

    reservations = Reservation.query.filter_by(user_id=user.id).all()
    if not reservations:
        return "No reservations found for this user."

    csv_file_name = f"user_{user.id}_reservations.csv"

    with open(f"exports/{csv_file_name}", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Reservation ID", "Lot Name", "Spot ID", "Vehicle No", "Parking Time", "Leaving Time", "Parking Cost"])

        for res in reservations:
            writer.writerow([
                res.id,
                res.spot.lot.name if res.spot and res.spot.lot else "N/A",
                res.spot_id,
                res.vehicle_number,
                res.parking_timestamp.strftime("%Y-%m-%d %H:%M:%S") if res.parking_timestamp else "N/A",
                res.leaving_timestamp.strftime("%Y-%m-%d %H:%M:%S") if res.leaving_timestamp else "N/A",
                res.parking_cost or 0
            ])

    return f"CSV exported successfully as {csv_file_name}"



@shared_task(ignore_results=False, name="monthly_parking_report")
def monthly_parking_report():
    users = User.query.filter_by(is_admin=False).all()
    for user in users:
        reservations = Reservation.query.filter_by(user_id=user.id).all()
        total_bookings = len(reservations)
        total_spent = sum(res.parking_cost or 0 for res in reservations)

        mail_template = """
        <h3>Hello {{ user.fullname }},</h3>
        <p>Here is your monthly SmartPark summary:</p>
        <table border="1" cellspacing="0" cellpadding="5">
            <tr><th>Total Bookings</th><td>{{ total_bookings }}</td></tr>
            <tr><th>Total Amount Spent (₹)</th><td>{{ total_spent }}</td></tr>
        </table>
        <p>Thank you for using SmartPark.</p>
        <h5>Regards,<br>SmartPark Team</h5>
        """

        message = Template(mail_template).render(
            user=user,
            total_bookings=total_bookings,
            total_spent=total_spent
        )

        send_email(user.email, subject="Monthly Parking Summary - SmartPark", message=message)

    return "Monthly parking reports sent to all users."



@shared_task(ignore_results=False, name="notify_user_booking")
def notify_user_booking(username, lot_name):
    text = f"Hi {username}, your parking spot at {lot_name} has been successfully booked. Thank you for using SmartPark!"
    webhook_url = "https://chat.googleapis.com/v1/spaces/AAQA7rWjjBI/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=5Ny4HP4xf7gx2mmhdfg4Y9-wTWA5xO3cYg2rawMUmmY"

    try:
        response = requests.post(webhook_url, json={"text": text})
        return f"Notification sent successfully (status code: {response.status_code})"
    except Exception as e:
        return f"Failed to send notification: {str(e)}"
