from backend.utils.helpers import take_screenshot

def capture_screenshot():
    filename = take_screenshot()
    return f"Screenshot taken and saved as {filename}"