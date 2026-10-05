from backend.utils.helpers import get_public_ip

def get_ip():
    ip = get_public_ip()
    return f"Your IP is {ip}"