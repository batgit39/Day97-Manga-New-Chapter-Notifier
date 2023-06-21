import smtplib

# NOTE: add your details
my_email = ""
password = ""


class MailSender:
    def __init__(self):
        self.my_email = my_email
        self.password = password

    def send_mail(self, message):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=self.my_email, password=self.password)
            connection.sendmail(
                from_addr=self.my_email,
                to_addrs=self.my_email,
                msg=message
            )
