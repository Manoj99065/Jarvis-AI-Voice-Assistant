import os
import platform
import subprocess
import datetime
import shutil

OS = platform.system()


# ============================================================
#  1. POWER OPERATIONS
# ============================================================
def shutdown():
    if OS == "Windows":
        os.system("shutdown /s /t 5")
    elif OS in ("Linux", "Darwin"):
        os.system("shutdown -h +5")
    else:
        return "Shutdown not supported."
    return "Shutting down your system in 5 seconds."

def restart():
    if OS == "Windows":
        os.system("shutdown /r /t 5")
    elif OS in ("Linux", "Darwin"):
        os.system("shutdown -r +5")
    else:
        return "Restart not supported."
    return "Restarting your system in 5 seconds."

def cancel_shutdown():
    if OS == "Windows":
        os.system("shutdown /a")
        return "Shutdown cancelled."
    elif OS in ("Linux", "Darwin"):
        os.system("shutdown -c")
        return "Shutdown cancelled."
    return "Cancel not supported."

def lock_screen():
    if OS == "Windows":
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "Screen locked."
    elif OS == "Linux":
        os.system("gnome-screensaver-command -l")
        return "Screen locked."
    elif OS == "Darwin":
        os.system("pmset displaysleepnow")
        return "Screen locked."
    return "Lock screen not supported."

def sleep_system():
    if OS == "Windows":
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "System going to sleep."
    elif OS == "Linux":
        os.system("systemctl suspend")
        return "System going to sleep."
    elif OS == "Darwin":
        os.system("pmset sleepnow")
        return "System going to sleep."
    return "Sleep not supported."

def hibernate():
    if OS == "Windows":
        os.system("shutdown /h")
        return "System hibernating."
    return "Hibernate only supported on Windows."


# ============================================================
#  2. APPLICATION CONTROL
# ============================================================
def open_app(app_name):
    try:
        if OS == "Windows":
            os.system(f"start {app_name}")
        elif OS == "Linux":
            subprocess.Popen([app_name])
        elif OS == "Darwin":
            subprocess.Popen(["open", "-a", app_name])
        return f"Opening {app_name}."
    except Exception as e:
        return f"Could not open {app_name}: {str(e)}"

def close_app(app_name):
    try:
        if OS == "Windows":
            os.system(f"taskkill /IM {app_name}.exe /F")
        else:
            os.system(f"pkill {app_name}")
        return f"Closed {app_name}."
    except Exception as e:
        return f"Could not close {app_name}: {str(e)}"


# ============================================================
#  3. FILE OPERATIONS
# ============================================================
def create_folder(path):
    try:
        os.makedirs(path, exist_ok=True)
        return f"Folder created at {path}."
    except Exception as e:
        return f"Could not create folder: {str(e)}"

def delete_file(path):
    try:
        if os.path.exists(path):
            os.remove(path)
            return f"Deleted {path}."
        return f"File not found: {path}"
    except Exception as e:
        return f"Could not delete file: {str(e)}"

def copy_file(source, destination):
    try:
        shutil.copy(source, destination)
        return f"Copied {source} to {destination}."
    except Exception as e:
        return f"Could not copy file: {str(e)}"

def move_file(source, destination):
    try:
        shutil.move(source, destination)
        return f"Moved {source} to {destination}."
    except Exception as e:
        return f"Could not move file: {str(e)}"

def list_files(path="."):
    try:
        files = os.listdir(path)
        return f"Files in {path}: {', '.join(files[:10])}"
    except Exception as e:
        return f"Could not list files: {str(e)}"


# ============================================================
#  4. SYSTEM INFO
# ============================================================
def get_system_info():
    try:
        return (f"OS: {platform.system()} {platform.version()} | "
                f"Processor: {platform.processor()} | "
                f"Hostname: {platform.node()}")
    except Exception as e:
        return f"Could not get system info: {str(e)}"

def get_battery():
    try:
        import psutil
        battery = psutil.sensors_battery()
        if battery:
            status = "charging" if battery.power_plugged else "not charging"
            return f"Battery is at {battery.percent}% ({status})."
        return "No battery detected."
    except ImportError:
        return "Please install psutil: pip install psutil"
    except Exception as e:
        return f"Could not get battery: {str(e)}"

def get_cpu_usage():
    try:
        import psutil
        return f"CPU usage is {psutil.cpu_percent(interval=1)}%."
    except ImportError:
        return "Please install psutil: pip install psutil"
    except Exception as e:
        return f"Could not get CPU usage: {str(e)}"

def get_ram_usage():
    try:
        import psutil
        ram = psutil.virtual_memory()
        used = round(ram.used / (1024**3), 2)
        total = round(ram.total / (1024**3), 2)
        return f"RAM usage is {ram.percent}% ({used} GB of {total} GB)."
    except ImportError:
        return "Please install psutil: pip install psutil"
    except Exception as e:
        return f"Could not get RAM usage: {str(e)}"

def get_disk_usage():
    try:
        import psutil
        disk = psutil.disk_usage('/')
        used = round(disk.used / (1024**3), 2)
        total = round(disk.total / (1024**3), 2)
        return f"Disk usage is {disk.percent}% ({used} GB of {total} GB)."
    except ImportError:
        return "Please install psutil: pip install psutil"
    except Exception as e:
        return f"Could not get disk usage: {str(e)}"


# ============================================================
#  5. NETWORK
# ============================================================
def get_wifi_password(ssid=None):
    try:
        if OS == "Windows":
            if ssid:
                result = subprocess.check_output(
                    f'netsh wlan show profile name="{ssid}" key=clear',
                    shell=True
                ).decode('utf-8', errors='ignore')
                for line in result.split('\n'):
                    if "Key Content" in line:
                        return f"WiFi password: {line.split(':')[1].strip()}"
                return "Password not found."
            else:
                result = subprocess.check_output(
                    'netsh wlan show profiles', shell=True
                ).decode('utf-8', errors='ignore')
                return f"Saved networks: {result[:300]}"
        return "Only supported on Windows."
    except Exception as e:
        return f"Could not get WiFi info: {str(e)}"

def toggle_wifi(state="on"):
    try:
        if OS == "Windows":
            if state == "off":
                os.system('netsh interface set interface "Wi-Fi" admin=disable')
                return "WiFi turned off."
            else:
                os.system('netsh interface set interface "Wi-Fi" admin=enable')
                return "WiFi turned on."
        return "Only supported on Windows."
    except Exception as e:
        return f"Could not toggle WiFi: {str(e)}"

def check_internet():
    try:
        import socket
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return "Internet is working."
    except Exception:
        return "No internet connection."


# ============================================================
#  6. PROCESS MANAGEMENT
# ============================================================
def list_processes():
    try:
        import psutil
        procs = [p.name() for p in psutil.process_iter()][:15]
        return f"Running processes: {', '.join(procs)}"
    except ImportError:
        return "Please install psutil: pip install psutil"
    except Exception as e:
        return f"Could not list processes: {str(e)}"

def kill_process(process_name):
    try:
        import psutil
        killed = 0
        for proc in psutil.process_iter(['name']):
            if process_name.lower() in proc.info['name'].lower():
                proc.kill()
                killed += 1
        if killed:
            return f"Killed {killed} process(es) named {process_name}."
        return f"No process found: {process_name}"
    except ImportError:
        return "Please install psutil: pip install psutil"
    except Exception as e:
        return f"Could not kill process: {str(e)}"


# ============================================================
#  7. DISPLAY
# ============================================================
def set_brightness(level):
    try:
        if OS == "Windows":
            import screen_brightness_control as sbc
            sbc.set_brightness(level)
            return f"Brightness set to {level}%."
        return "Only supported on Windows."
    except ImportError:
        return "Please install: pip install screen-brightness-control"
    except Exception as e:
        return f"Could not set brightness: {str(e)}"

def empty_recycle_bin():
    try:
        if OS == "Windows":
            os.system('PowerShell.exe -Command "Clear-RecycleBin -Force"')
            return "Recycle bin emptied."
        return "Only supported on Windows."
    except Exception as e:
        return f"Could not empty recycle bin: {str(e)}"


# ============================================================
#  8. TERMINAL
# ============================================================
def run_command(command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return result.decode('utf-8', errors='ignore')[:500]
    except Exception as e:
        return f"Command failed: {str(e)}"

def open_cmd():
    try:
        if OS == "Windows":
            os.system("start cmd")
        elif OS == "Linux":
            os.system("gnome-terminal")
        elif OS == "Darwin":
            os.system("open -a Terminal")
        return "Terminal opened."
    except Exception as e:
        return f"Could not open terminal: {str(e)}"


# ============================================================
#  9. TIME & DATE
# ============================================================
def get_time():
    return f"Current time: {datetime.datetime.now().strftime('%I:%M %p')}"

def get_date():
    return f"Today's date: {datetime.datetime.now().strftime('%A, %d %B %Y')}"