import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
import smtplib
from backend.utils.config import Config

def send_email(recipient, content):
    """Send email using Gmail SMTP."""
    if not Config.EMAIL_ADDRESS or not Config.EMAIL_PASSWORD:
        return "Email credentials not configured."
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(Config.EMAIL_ADDRESS, Config.EMAIL_PASSWORD)
        server.sendmail(Config.EMAIL_ADDRESS, recipient, content)
        server.close()
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False