import network
import time

class NetworkManager:
    def __init__(self, ssid, password, ip_address=None, netmask="255.255.255.0", gateway="192.168.88.1", dns="8.8.8.8"):
        self.ssid = ssid
        self.password = password
        self.ip_address = ip_address
        self.netmask = netmask
        self.gateway = gateway
        self.dns = dns
        self.wlan = network.WLAN(network.STA_IF)

    def connect_to_wifi(self, timeout=10):
        try:
            self.wlan.active(True)

            if self.ip_address:
                print(f"[Wi-Fi] Using static IP: {self.ip_address}")
                self.wlan.ifconfig((self.ip_address, self.netmask, self.gateway, self.dns))
            else:
                print("[Wi-Fi] Using DHCP")

            self.wlan.connect(self.ssid, self.password)

            start_time = time.time()
            while not self.wlan.isconnected():
                if time.time() - start_time > timeout:
                    print("[Wi-Fi] Connection timed out.")
                    return False
                time.sleep(0.5)

            print("[Wi-Fi] Connected successfully")
            print("[Wi-Fi] IP Address:", self.wlan.ifconfig()[0])
            return True

        except Exception as e:
            print("[Wi-Fi] Connection error:", e)
            return False

    def is_connected(self, timeout=10):
        try:
            start_time = time.time()
            while time.time() - start_time < timeout:
                if self.wlan.isconnected():
                    return True
                time.sleep(0.5)
            return False
        except Exception as e:
            print("[Wi-Fi] Status check error:", e)
            return False

