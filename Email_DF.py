#! python

# Email a dataframe in table format

# Import modules
import smtplib                                          # For Sending emails
from email.mime.text import MIMEText                    # MIME helps us format emails
from email.mime.application import MIMEApplication      # MIME also allows us to email data in a tabular (or DF) format 
from email.mime.multipart import MIMEMultipart          

# Email a dataframe function

def email_df(data, host='', email='', pw='', recipients=[], subject='', From=''):
    '''
    Takes a dataframe and emails it to recipients.
        Parameters:
                data: dataframe
                host: should be 'smtp.yourdomain.com'
                email: your email address
                pw: password for your email address (passing env variables is recommended)
                recipients: list of emails to send to (must be str)
                subject: what you want the subject line to be
                From: who the email is coming from (typically same as host)
        Returns:
            None.
        Notes:
            Must pass a dataframe.
    '''
    emaillist = [elem.strip().split(',') for elem in recipients] # Parse recipients list

    msg = MIMEMultipart()                                        # Variable to initiate the MIME function for inputting different pieces of the email
    msg['Subject'] = subject                                     # Subject line
    msg['From'] = From                                           # Who the email is being sent from (probably same as the email variable)
    
    # This formats the DF into an html format

    html = """\
    <html>
        <head></head>
        <body>
        {0}
        </body>
    </html>
    """.format(data.to_html())                                    # This is what allows the DF to appear as a table in the email
                                                                    # Note the data.to_html method

    part1 = MIMEText(html, 'html')                                # Further html formatting
    msg.attach(part1)

                                                                    # The bit that actually sends the email

    con = smtplib.SMTP(host, 587)                                 # Connection variable
    con.ehlo()                                                    # Starts the connection
    con.starttls()                                                # Starts the encryption
    con.login(email, pw)                                          # Logs you in
    con.sendmail(msg['From'], emaillist , msg.as_string())        # Sends your email
    con.quit()
    return
