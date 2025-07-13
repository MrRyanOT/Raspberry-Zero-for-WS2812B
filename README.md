sudo apt install python3-pip -y


sudo apt install build-essential python3-dev scons -y

sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel --break-system-packages

chmod +x /home/raspberry/artnet_led.py

sudo systemctl daemon-reload

sudo systemctl enable artnet.service

sudo systemctl start artnet.service

systemctl status artnet.service

sudo nano /boot/firmware/config.txt

dtparam=audio=off

sudo nano /etc/systemd/system/artnet.service
