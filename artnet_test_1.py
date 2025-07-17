import network
import socket
import time

# ====== NETWORK CONFIG ======
SSID = '((( Friday )))'
PASSWORD = '0004edb6700b6'
STATIC_IP = '192.168.88.102'         # Use None or "" for DHCP
NETMASK = '255.255.255.0'
GATEWAY = '192.168.88.1'
DNS = '8.8.8.8'

# ====== ART-NET CONFIG ======
ARTNET_PORT = 6454
UNIVERSE = 0                         # Change if your sender uses a different one

# ====== Wi-Fi Connection ======
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if STATIC_IP:
    print("[WiFi] Setting static IP:", STATIC_IP)
    wlan.ifconfig((STATIC_IP, NETMASK, GATEWAY, DNS))

print("[WiFi] Connecting to network...")
wlan.connect(SSID, PASSWORD)

start = time.ticks_ms()
while not wlan.isconnected():
    if time.ticks_diff(time.ticks_ms(), start) > 10000:
        print("[WiFi] Connection timed out.")
        raise SystemExit
    time.sleep(0.25)

ip = wlan.ifconfig()[0]
print("[WiFi] Connected. IP assigned:", ip)

# ====== Socket Setup ======
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, ARTNET_PORT))     # Bind directly to device IP
sock.setblocking(False)          # Non-blocking mode for MicroPython

print(f"[Art-Net] Listening on {ip}:{ARTNET_PORT} for ArtDMX packets...")

# ====== DMX Packet Loop ======
while True:
    try:
        try:
            data, addr = sock.recvfrom(1024)
        except OSError:
            data = None

        if data:
            if data[0:8] == b'Art-Net\x00' and data[8:10] == b'\x00\x50':  # ArtDMX opcode
                universe = data[14] + (data[15] << 8)
                length = (data[16] << 8) + data[17]
                dmxdata = data[18:18 + length]

                print(f"\n🎛 Packet from {addr}")
                print(f"🔀 Universe: {universe}")
                print(f"📦 DMX Length: {length} bytes")

                if universe == UNIVERSE:
                    print(f"🧬 First 12 DMX values: {list(dmxdata[:12])}")
                else:
                    print(f"⚠️ Packet not for universe {UNIVERSE}, ignoring.")
        time.sleep(0.01)
    except Exception as e:
        print("[Art-Net] Error:", e)
        time.sleep(1)

