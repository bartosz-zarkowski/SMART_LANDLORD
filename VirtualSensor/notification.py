import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def sendEmail(receiver_email,email_password):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "smartlandlordzut@gmail.com"
    
    message = MIMEMultipart('alternative')
    message["Subject"] = "Alert Mieszkania"
    message["From"] = sender_email
    message["To"] = receiver_email

    html="""\
            <html>
                <body>
                    Wiadomosc dotyczaca mieszkania
                    <div style="color:red;font-size:30px;">
                    Test
                    </div>

                    <div style="color:pink;font-size:20px;">
                    Test
                    </div>
                </body>
            </html>
        """
    
    part2=MIMEText(html,"html")

    message.attach(part2)
    


    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, email_password)
        server.sendmail(sender_email, receiver_email, message.as_string())