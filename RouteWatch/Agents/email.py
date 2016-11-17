import smtplib
from email.mime.text import MIMEText
from email.utils import COMMASPACE

from RouteWatch.DB.client import DB as database
from RouteWatch.Security.crypto import decrypt


DB = database()


def email(changes, to, secret):
    """
    A simplistic run-of-the-mill mailing list handler
    :param changes:
    :type changes: list
    :param to:
    :type to: list
    :param secret:
    :type secret: bytes
    :return: None
    """
    # Retrieve credentials from DB
    encrypted_from_addr = DB.get("Settings", name="email_address")[0]
    encrypted_username = DB.get("Settings", name="email_user")[0]
    encrypted_password = DB.get("Settings", name="email_password")[0]
    encrypted_server = DB.get("Settings", name="email_server")[0]
    # Decrypt credentials
    from_addr = decrypt(encrypted_from_addr.data.encode(), secret).decode()
    mail_username = decrypt(encrypted_username.data.encode(), secret).decode()
    mail_password = decrypt(encrypted_password.data.encode(), secret).decode()
    mail_server = decrypt(encrypted_server.data.encode(), secret).decode()
    # Compile the message
    msg = MIMEText(
        '''
        <B><H2>Something is happening!!!</H2></B>
        <H3>
        {}
        </H3>
        '''.format("<br>".join(changes)),
        "html")
    msg['Subject'] = 'Changes to network visibility have occurred'
    msg['From'] = "RouteWatch <{}>".format(from_addr)
    msg['To'] = COMMASPACE.join(to)
    # Send the message via our SMTP server.
    s = smtplib.SMTP(mail_server)
    # Say Hello
    s.ehlo()
    # Secure the connection
    s.starttls()
    # Say Hello to the secure channel
    s.ehlo()
    # Login
    s.login(mail_username, mail_password)
    # Send the e-mail(s)
    s.send_message(msg)
    # Cleanly disconnect
    s.quit()