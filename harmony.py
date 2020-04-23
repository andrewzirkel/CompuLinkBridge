import compulink
import threading
from evdev import InputDevice, ecodes, list_devices
from time import sleep


# Kick off threads to listen to harmony input devices
class Harmony(object):
    threads = list()

    def get_harmony_devices(self):
        harmony_devices = list()
        devices = [InputDevice(path) for path in list_devices()]
        for device in devices:
            if device.name == "Harmony Keyboard Keyboard" or device.name == "Harmony Keyboard Consumer Control":
                harmony_devices.append(device.path)
        return harmony_devices

    def spawn_listener(self, dev):
        listener = HarmonyListener(dev)
        listener.listen()

    def listen(self):
        current_devices = list()
        while 1:
            # loop to grab new devices
            new_devices = list(set(list_devices()) - set(current_devices))
            current_devices = list_devices()
            for device in new_devices:
                device = InputDevice(device)
                if "Harmony" in device.name:
                    x = threading.Thread(target=self.spawn_listener, args=(device.path,))
                    self.threads.append(x)
                    x.start()
                sleep(.5)


# listen to one harmony input device and push out to compulink
class HarmonyListener(object):
    debug = 1
    playpauselastkey = "KEY_PAUSE"
    mycompulink = compulink.CompuLink(18)
    keycode_compulink_map = {
        "KEY_EJECTCD": [4, 0],  # Eject - 161
        "KEY_PLAY": [4, 1],  # Play - 207
        "KEY_STOPCD": [4, 2],  # Stop
        "KEY_NEXTSONG": [4, 3],  # Next track
        "KEY_PREVIOUSSONG": [4, 4],  # Previous track
        "KEY_PAUSE": [4, 5],  # Pause - 119
        "KEY_FASTFORWARD": [4, 8],  # Seek Forward
        "KEY_REWIND": [4, 9],  # Seek Back
        "KEY_1": [5, 1],  # Track 1
        "KEY_2": [5, 2],  # Track 2
        "KEY_3": [5, 3],  # Track 3
        "KEY_4": [5, 4],  # Track 4
        "KEY_5": [5, 5],  # Track 5
        "KEY_6": [5, 6],  # Track 6
        "KEY_7": [5, 7],  # Track 7
        "KEY_8": [5, 8],  # Track 8
        "KEY_9": [5, 9],  # Track 9
        "KEY_0": [5, 11]  # Track 10
    }

    # keep track of playpause because media center remote doesn't send the correct keys...yet
    def playpause(self):
        if "KEY_PLAY" == self.playpauselastkey:
            self.playpauselastkey = "KEY_PAUSE"
            return "KEY_PAUSE"
        else:
            self.playpauselastkey = "KEY_PLAY"
            return "KEY_PLAY"

    def map_codes(self, code):
        if "KEY_PLAYPAUSE" == code:
            code = self.playpause()
        if "KEY_STOPCD" == code:
            self.playpauselastkey = "KEY_PAUSE"
        return self.keycode_compulink_map.get(code)

    def send_command(self, command_pair):
        self.mycompulink.sendCommand(command_pair[1], command_pair[0])

    def listen(self):
        try:
            for event in self.dev.read_loop():
                if event.type != ecodes.EV_KEY:
                    continue
                # skip up events
                if event.value == 0:
                    continue
                code = ecodes.bytype[event.type][event.code]
                command_pair = self.map_codes(code)
                if command_pair:
                    print "Got Code: " + code + " Sending: " + str(command_pair[0]) + "." + str(command_pair[1]) + \
                          ' to compulink bus '
                    self.send_command(command_pair)
                else:
                    print (code + " not found.")
        except:
            return

    def __init__(self, devpath):
        self.dev = InputDevice(devpath)
        self.dev.grab()

    def __del__(self):
        self.dev.ungrab()
