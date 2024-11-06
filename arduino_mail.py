import serial
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Setup Serial Communication
arduino_port = 'COM8' 
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate)

# Email Configuration
sender_email = "reportdefibrillator@gmail.com"
receiver_email = "pharesw10@gmail.com"
password = "xrrv xjhe ruun zade"

# SMTP Configuration
smtp_server = "smtp.gmail.com"  # e.g., smtp.gmail.com for Gmail
smtp_port = 587  # Standard SMTP port

def send_email():
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Defibrillator Report"

    body = "Pin 7 on your Arduino is currently HIGH."
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Listen to Serial and trigger email
while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        print(f"Received: {line}")
        if line == "HIGH":
            send_email()
