from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioMeterInformation
import time

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioMeterInformation._iid_, CLSCTX_ALL, None
)
meter = interface.QueryInterface(IAudioMeterInformation)

# meter = AudioUtilities.GetAudioSessionManager

try:
    while True:
        bar = "|"+"|" * int(meter.GetPeakValue() * 500)
        print(f"{bar}\n\r", end="")
        # print(f"Current master peak level: {meter.GetPeakValue():.2f}\r", end="")
        time.sleep(0.1)
except KeyboardInterrupt:
    pass

