import datetime

def get_current_time():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    return f"Sir, the time is {now}"