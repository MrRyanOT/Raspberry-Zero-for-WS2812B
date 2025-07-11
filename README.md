import time
from rpi_ws281x import PixelStrip, Color

# LED strip configuration:
LED_COUNT = 60    	# Number of LED pixels.
LED_PIN = 18      	# GPIO pin connected to the pixels (must support PWM).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800kHz).
LED_DMA = 10      	# DMA channel to use for generating signal (try 10).
LED_BRIGHTNESS = 255  # Brightness (0 to 255).
LED_INVERT = False	# True to invert the signal.
LED_CHANNEL = 0   	# Set to 1 for GPIO13 if used.

# Create PixelStrip object.
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
    	return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
    	pos -= 85
    	return Color(255 - pos * 3, 0, pos * 3)
	else:
    	pos -= 170
    	return Color(0, pos * 3, 255 - pos * 3)

def rainbow_cycle(strip, wait_ms=20, iterations=5):
	"""Draw rainbow that cycles across all pixels."""
	for j in range(256 * iterations):
    	for i in range(strip.numPixels()):
        	pixel_index = (i * 256 // strip.numPixels()) + j
        	strip.setPixelColor(i, wheel(pixel_index & 255))
    	strip.show()
    	time.sleep(wait_ms / 1000.0)

try:
	print("🌈 Rainbow cycle starting. Press Ctrl+C to stop.")
	rainbow_cycle(strip)
except KeyboardInterrupt:
	print("\nStopping, clearing LEDs.")
	for i in range(strip.numPixels()):
    	strip.setPixelColor(i, Color(0, 0, 0))
	strip.show()


sudo apt install python3-pip -y


sudo apt install build-essential python3-dev scons -y

sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel --break-system-packages

chmod +x /home/raspberry/artnet_led.py

sudo nano /etc/systemd/system/artnet.service

[Unit]
Description=Art-Net LED Controller
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/raspberry/artnet_led.py
WorkingDirectory=/home/raspberry
StandardOutput=inherit
StandardError=inherit
Restart=always
User=root

[Install]
WantedBy=multi-user.target

sudo systemctl daemon-reload

sudo systemctl enable artnet.service

sudo systemctl start artnet.service

systemctl status artnet.service

sudo nano /boot/firmware/config.txt

dtparam=audio=off








Lets make sure that the folowing gets run after boot

import socket
import time
from rpi_ws281x import PixelStrip, Color

# CONFIGURATION
LED_COUNT = 60
LED_PIN = 18
strip = PixelStrip(LED_COUNT, LED_PIN)
strip.begin()

# ARTNET
ARTNET_PORT = 6454
UNIVERSE = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', ARTNET_PORT))
sock.settimeout(0.1)

def parse_artnet_packet(data):
	if len(data) < 18: return None, None
	if data[:8] != b'Art-Net\x00': return None, None
	opcode = int.from_bytes(data[8:10], 'little')
	if opcode != 0x5000: return None, None
	universe = int.from_bytes(data[14:16], 'little')
	length = int.from_bytes(data[16:18], 'big')
	dmx_data = data[18:18+length]
	return universe, dmx_data

def update_strip(dmx_data):
	for i in range(min(LED_COUNT, len(dmx_data)//3)):
    	r = dmx_data[i*3]
    	g = dmx_data[i*3+1]
    	b = dmx_data[i*3+2]
    	strip.setPixelColor(i, Color(r, g, b))
	strip.show()

print("✅ Art-Net LED Controller started. Listening for data...")

while True:
	try:
    	data, addr = sock.recvfrom(1024)
    	universe, dmx_data = parse_artnet_packet(data)
    	if universe == UNIVERSE:
        	print(f"🎛 Received Universe: {universe}, Data Length: {len(dmx_data)} bytes" )
        	print("First 12 bytes (4 RGB channels):", list(dmx_data[:12]))
        	update_strip(dmx_data)
	except socket.timeout:
    	pass
	except Exception as e:
    	print("⚠️ Error:", e)





