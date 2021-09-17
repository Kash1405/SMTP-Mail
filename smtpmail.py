import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SmtpMail:
    
    # Contains email contents, connection settings and recipient settings.
    # Default SMTP server used: Gmail server
    # Default Connection: TLS
    # NOTE: DIFFERENT PORTS USED FOR TLS AND SSL

    def __init__(self, username, password, server=("smtp.gmail.com",587), use_SSL = False):

        self.username = username
        self.password = password
        self.server_name = server[0]
        self.server_port = server[1]
        self.use_SSL = use_SSL

        # Checking if SSL connection
        if self.use_SSL == False:
            self.smtpserver = smtplib.SMTP(self.server_name, self.server_port)
        else:
            self.smtpserver = smtplib.SMTP_SSL(self.server_name, self.server_port)

        self.connected = False
        self.recipients = []


    def __str__(self):
        return  "Connection to server {}, port {} \nConnected: {} \nUsername: {}, Password: {}".format(self.server_name, self.server_port, self.connected, self.username, self.password)
        
    def set_message(self, plaintext, subject="", input_from=None, htmltext=None):

        # Creation of MIME Message
        self.html_ready = False

        if htmltext is not None:
            self.html_ready = True
        else:
            self.htmlready = False
        
        if self.html_ready:
            self.msg = MIMEMultipart('alernative')
            self.msg.attach(MIMEText(plaintext,'plain'))
            self.msg.attach(MIMEText(htmltext,'html'))
        else:
            self.msg = MIMEText(plaintext,'plain')

        self.msg['Subject'] = subject
        if input_from == None:
            self.msg['From'] = self.username
        else:
            self.msg['From'] = input_from
        
        self.msg['To'] = None
        self.msg['CC'] = None
        self.msg['BCC'] = None
        
    def clear_message(self):

        self.msg.set_payload("")

    def set_subject(self,subject):

        self.msg.replace_header("Subject", subject)

    def set_from(self,input_from):
        
        self.msg.replace_header("From", input_from)

    def set_html(self, html):

        try:
            payload = self.msg.get_payload()
            payload[1] = MIMEText(html,'html')
            self.msg.set_payload(payload)

        except TypeError:
            print("Error: Payload is not a list.")

        raise

    def set_recipients(self, recipients):

        if not isinstance(recipients, (list, tuple)):
            raise TypeError("Recipients must be a list or tuple.")

        self.recipients = recipients
    
    def add_recipient(self, recipient):

        self.recipients.append(recipient)

    def connect(self):
         
        if not self.use_SSL:
            self.smtpserver.starttls()
        
        self.smtpserver.login(self.username,self.password)
        self.connected = True
        print("Connected")

    def disconnect(self):

        self.smtpserver.close()
        self.connected = False

    def send_mail(self, connection_close = True):

        if not self.connected:
            raise ConnectionError("Not Connected to any server.")

        print("Message: {}".format(self.msg.get_payload()))

        for recipient in self.recipients:
            self.msg.replace_header("To", recipient)
            print("Sending to {}".format(recipient))
            self.smtpserver.send_message(self.msg)
            
        print("Mails delivered to all.")
    
        if connection_close:
            self.disconnect()
            print("Connection Closed.")