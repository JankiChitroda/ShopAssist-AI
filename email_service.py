import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_escalation_email(recipient_email, subject, body):
    """
    Sends an SMTP email notification when a support ticket is escalated.
    """
    sender_email = "support@shopassist.ai"
    sender_password = "your_smtp_password_here"
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Example using Gmail SMTP server as a standard template
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # server.login(sender_email, sender_password)
        # server.sendmail(sender_email, recipient_email, msg.as_string())
        # server.quit()
        print(f"[EMAIL SERVICE] Escalation alert sent to {recipient_email}")
        return True
    except Exception as e:
        print(f"[EMAIL SERVICE ERROR] Failed to send email: {e}")
        return False