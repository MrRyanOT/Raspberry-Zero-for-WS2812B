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
