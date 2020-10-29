import smtplib                  # the library we use to connect to an email server

host = 'smtp.gmail.com'         # smtp connection domain. In this case we are using gmail.

con = smtplib.SMTP(host, 587)   # this is the connection variable, 587 is the port number
con.ehlo()                      # start the connection
con.starttls()                  # starts encryption

email = 'email@domain.com'      # replace this with your login email for your credentials
pw = '********'                 # replace this with your password

con.login(email, pw)            # logins you into your account

to = 'email@domain.com'                                       # this is the email you are sending from. It will likely be the same as the email variable above
subject = 'Subject: Your_Subject\n\n'                                # this is the subject line and it must start with 'Subject: '
body = 'Hello,\n\nThis is an email from Python.\n\n-Ken'      # this is your message body

con.sendmail(email, to, subject+body)   # sends your email

con.quit()                              # ends the connection
