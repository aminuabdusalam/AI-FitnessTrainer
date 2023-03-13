import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def report_sender(recipient_email, minutes_exercised, calories_burned):
    # Set up the email message
    sender_email = "your-email@example.com"
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = 'Exercise Report'

    # Construct the HTML text for the message body
    # hours_exercised = 1.5
    html = f"""
    <html>
    <body>
        <h2>Exercise Report</h2>
        <p>You spent {minutes_exercised} minutes exercising today and burned {calories_burned} calories.</p>
        <p>Here are some recommendations for your next workout:</p>
        <ul>
        <li>You may want to increase your exercise time to 2 hours.</li>
        <li>Do some cardio exercises to improve your heart health</li>
        <li>Incorporate strength training to build muscle and bone density</li>
        <li>Try some yoga or stretching to increase flexibility</li>
        </ul>
    </body>
    </html>
    """



    # Add the HTML text to the message body
    body = MIMEText(html, 'html')
    message.attach(body)

    # Send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('your-email@example.com', 'your-email-password')
        text = message.as_string()
        server.sendmail(sender_email, recipient_email, text)

        