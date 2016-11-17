import smtplib
from email.mime.text import MIMEText
from email.utils import COMMASPACE

from RouteWatch.DB.client import DB as database
from RouteWatch.Security.crypto import decrypt


DB = database()


def email(changes, to, secret):
    encrypted_from_addr = DB.get("Settings", name="email_address")[0]
    encrypted_username = DB.get("Settings", name="email_user")[0]
    encrypted_password = DB.get("Settings", name="email_password")[0]
    encrypted_server = DB.get("Settings", name="email_server")[0]
    from_addr = decrypt(encrypted_from_addr.data.encode(), secret).decode()
    mail_username = decrypt(encrypted_username.data.encode(), secret).decode()
    mail_password = decrypt(encrypted_password.data.encode(), secret).decode()
    mail_server = decrypt(encrypted_server.data.encode(), secret).decode()
    msg = MIMEText(
    '''
    <B><H2>Something is happening!!!</H2></B>
    {}
    '''.format("<br>".join(changes))
    , "html")


    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = 'Changes to network visibility have occurred'
    msg['From'] = "RouteWatch <{}>".format(from_addr)
    msg['To'] = COMMASPACE.join(to)
    print(msg)
    # Send the message via our own SMTP server.
    s = smtplib.SMTP(mail_server)
    print("Connection made")
    s.ehlo()
    print("EHLO")
    s.starttls()
    print("StartTLS")
    s.ehlo()
    print("EHLO")
    s.login(mail_username, mail_password)
    print("Logged in")
    s.send_message(msg)
    print("Message sent")
    s.quit()