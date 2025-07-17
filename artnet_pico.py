import network
import socket
import time
import machine
import neopixel
from machine import Pin

# ====== CONFIG ======
SSID = 'YourWiFiSSID'
PASSWORD = 'YourWiFiPassword'
LED_PIN = 0          # GP0
NUM_LEDS = 60        # Your LED count
UNIVERSE = 0         # Universe number expected

# ====== WiFi Connect ======
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Connecting to WiFi...", end="")
while not wlan.isconnected():
    print(".", end="")
    time.sleep(0.5)
print("Connected with IP:", wlan.ifconfig()[0])

# ====== Setup LEDs ======
np = neopixel.NeoPixel(Pin(LED_PIN), NUM_LEDS)

# ====== Setup UDP Socket ======
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 6454))  # Art-Net default port

print("Listening for Art-Net data...")

# ====== Art-Net Listener Loop ======
while True:
    data, addr = sock.recvfrom(1024)

    if data[0:8] == b'Art-Net\x00' and data[8:10] == b'\x00\x50':  # OpCode ArtDMX
        universe = data[14] + (data[15] << 8)
        length = (data[16] << 8) + data[17]
        dmxdata = data[18:18+length]

        if universe == UNIVERSE:
            # Update LEDs
            for i in range(NUM_LEDS):
                if (i*3 + 2) < len(dmxdata):
                    r = dmxdata[i*3]
                    g = dmxdata[i*3+1]
                    b = dmxdata[i*3+2]
                    np[i] = (g, r, b)  # WS2812 expects GRB
            np.write()
