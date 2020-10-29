#!python

# Import packages
import smtplib

# Email a dataframe function

def send_email(subject='', body='', host='', email='', pw='', recipients=[]):
    '''
    Takes some test (body) and emails it to recipients.
        Parameters:
                subject: what you want the subject line to be
                body: what you want to say
                host: should be 'smtp.yourdomain.com'
                email: your email address
                pw: password for your email address (passing env variables is recommended)
                recipients: list of emails to send to (must be strings within a list)
        Returns:
            None.
        Notes:
        body should be formatted using \\n for new lines. 
        E.g., Hello,\\n\\nThis is an email from Python.\\n\\n-Ken
    '''
    emaillist = [elem.strip().split(',') for elem in recipients]  # Parses recipients list
    
    subject = 'Subject: '+subject+'\n\n'                            
    body = 'Hello,\n\n'+body

    con = smtplib.SMTP(host, 587)                                 # Connection variable
    con.ehlo()                                                    # Starts the connection
    con.starttls()                                                # Starts the encryption
    con.login(email, pw)                                          # Logs you in
    con.sendmail(email, emaillist, subject+body)                  # Sends your email
    con.quit()
    return
