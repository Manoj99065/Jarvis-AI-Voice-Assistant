
import pythoncom
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


def change_volume(delta):
    """
    Change system volume by delta (e.g., 0.1 = +10%, -0.1 = -10%).
    Returns new volume as float (0.0 - 1.0) or None on failure.
    """
    try:
        # 👇 YEH LINE ZAROORI HAI — thread mein COM initialize karo
        pythoncom.CoInitialize()

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None
        )
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        current = volume.GetMasterVolumeLevelScalar()
        new_vol = max(0.0, min(1.0, current + delta))
        volume.SetMasterVolumeLevelScalar(new_vol, None)

        # 👇 COM cleanup
        pythoncom.CoUninitialize()
        return new_vol
    except Exception as e:
        # Ensure cleanup even on failure
        try:
            pythoncom.CoUninitialize()
        except:
            pass
        print(f"Volume error: {e}")
        return None


def get_volume():
    """Get current system volume (0.0 - 1.0)."""
    try:
        pythoncom.CoInitialize()
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None
        )
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        current = volume.GetMasterVolumeLevelScalar()
        pythoncom.CoUninitialize()
        return current
    except Exception as e:
        print(f"Volume error: {e}")
        return None


def set_volume(level):
    """Set volume to a specific level (0.0 - 1.0)."""
    try:
        pythoncom.CoInitialize()
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None
        )
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(max(0.0, min(1.0, level)), None)
        pythoncom.CoUninitialize()
        return level
    except Exception as e:
        print(f"Volume error: {e}")
        return None