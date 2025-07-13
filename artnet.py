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
