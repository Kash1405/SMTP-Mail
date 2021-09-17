from smtpmail import SmtpMail

'''INPUT VALUES HERE'''
userid= '<<PLACE USERID>>'
password = '<<PLACE PASSWORD>>'
mail_body = "Dear Sir, \n" \
            "This is a test. Thank you for your patience.\n" \
            "Yours Sincerely,\n"\
            "John Doe"
list_of_recipients = ['<<ID1>>','<<ID2>>',"..."]

plaintext = mail_body

ourSmtpMail = SmtpMail('userid', 'password', ('smtp.gmail.com', 587))

ourSmtpMail.set_message(plaintext, "This is a test", "AK")

ourSmtpMail.set_recipients(list_of_recipients)

ourSmtpMail.connect()

ourSmtpMail.send_mail()
