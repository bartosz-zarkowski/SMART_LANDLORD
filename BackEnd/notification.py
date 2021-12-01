import smtplib, ssl

def sendEmail(receiver_email,email_password):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "smartlandlordzut@gmail.com"
    message = """\
    Wystapil problem w mieszkaniu na ulicy abc.
    Problem: Duży pobór prądu przez godzinę."""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, email_password)
        server.sendmail(sender_email, receiver_email, message)