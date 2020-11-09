#! python

# Python cide for sending email with attachments 
# from your Gmail account

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

def email_attach(filename='', filepath='', host='', email='', pw='', subject='', body='', to=''):
    '''
    Takes some text (body) and a file and sends an email with the file attached.
        Parameters:
                filename: filename with extension (e.g., 'file.xlsx')
                filepath: full file path with filename included
                host: should be 'smtp.yourdomain.com'
                email: your email address
                pw: password for your email address (passing env variables is recommended)
                subject: what you want the subject line to be
                body: what you want to say
        Returns:
            None.
    '''
    msg = MIMEMultipart()                #instance of MIMEMultipart
    msg['From'] = email                  #storing the senders email address
    msg['To'] = to                       #storing the receivers email
    msg['Subject'] = subject             #storing the subject
    body = body
    msg.attach(MIMEText(body, 'plain'))  #attached the body with the msg instance

    attachment = open(filepath, "rb")    #open the file to be sent

    p = MIMEBase('application', 'octet-stream')  #instance of MIMEBase and named as p 
    p.set_payload((attachment).read())           #to change the payload into encoded form 
  
    encoders.encode_base64(p)                    #encode into base64 
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
  
    msg.attach(p)                          #attach the instance 'p' to instance 'msg' 
  
    s = smtplib.SMTP(host, 587)            #creates SMTP session 
    s.starttls()                           #start TLS for security 
    s.login(email, pw)                     #authentication
  
    text = msg.as_string()                 #converts the Multipart msg into a string 
  
    s.sendmail(email, to, text)            #sending the email 
  
    s.quit()                               #terminating the session 
    return
