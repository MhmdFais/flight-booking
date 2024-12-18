import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging


class NotificationAgent:
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self.smtp_server = "smtp.gmail.com" #Using gmail
        self.smtp_port = 465
        self.sender_email = sender_email  # need an email
        self.sender_password = sender_password

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def send_notification(self, recipient_email, subject, message_body):
        try:
            message = MIMEMultipart()
            message['From'] = self.sender_email
            message['To'] = recipient_email
            message['Subject'] = subject

            message.attach(MIMEText(message_body, 'plain'))

            # Secure SSL connection
            context = ssl.create_default_context()

            # Send the email
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())

            self.logger.info(f'Notification sent successfully to {recipient_email}')
            return True

        except Exception as e:
            self.logger.error('Failed to send notification')
            return False

    def send_booking_notification(self, recipient_email, booking_details):
        subject = f"Booking Confirmation - {booking_details.get('booking_reference', 'N/A')}"

        message_body = f"""
        Dear Passenger,

        Your booking has been confirmed.

        Booking details:
         - Booking Reference: {booking_details.get('booking_reference', 'N/A')}
         - Flight: {booking_details.get('flight', 'N/A')}
         - Departure: {booking_details.get('departure_city', 'N/A')} on {booking_details.get('departure_date', 'N/A')}
         - Destination: {booking_details.get('destination_city', 'N/A')}

        Thank you for choosing us.
        """
        return self.send_notification(recipient_email, subject, message_body)

    def send_payment_notification(self, recipient_email, payment_details):
        status = "Successful" if payment_details.get('status', False) else "Failed"
        subject = f"Payment {status} - Booking {payment_details.get('booking_reference', 'N/A')}"

        message_body = f"""
        Dear Passenger,

        Your payment status:
            - Status: {status}
            - Booking Reference: {payment_details.get('booking_reference', 'N/A')}
            - Amount: {payment_details.get('amount', 'N/A')}

        {"Payment processed successfully." if status == "Successful" else "Please retry your payment."}
        """
        return self.send_notification(recipient_email, subject, message_body)

    def send_booking_cancel_notification(self, recipient_email, cancellation_details):
        subject = f"Booking Cancelled - {cancellation_details.get('booking_reference', 'N/A')}"

        message_body = f"""
            Dear Passenger,
            Your following booking has been cancelled.
            
            Cancellation details:
             - Booking Reference: {cancellation_details.get('booking_reference', 'N/A')}
             - Flight: {cancellation_details.get('flight', 'N/A')}
             - Departure: {cancellation_details.get('departure_city', 'N/A')}
             - Destination: {cancellation_details.get('destination_city', 'N/A')}
             
            Your booking cancellation processed successfully.
        """

        return self.send_notification(recipient_email, subject, message_body)
