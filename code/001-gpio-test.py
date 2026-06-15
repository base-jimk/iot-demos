import time  # used for sleep function
import gpiod # used for gpio control

# select the gpio control chip. Should be chip0 for Rpi 5 with July2024 update; chip4 for older Rpi5
chip = gpiod.Chip("/dev/gpiochip0")

# Select your gpio pin connected to your electronic component (e.g. LED)
gpioPin = 17

# Reserve access to GPIO control line for pin #17
request = chip.request_lines(
	consumer="test",
	config={
		gpioPin: gpiod.LineSettings(
		direction=gpiod.line.Direction.OUTPUT)
		}
)

# Set the control line 'Active' to turn on the LED (voltage = 3.3V)
print("LED ON")
request.set_value(gpioPin,gpiod.line.Value.ACTIVE
)

# 5 second delay
time.sleep(5)

# Set the control line 'Inactive' to turn off the LED (voltage = 0V)
print("LED OFF")
request.set_value(gpioPin,gpiod.line.Value.INACTIVE)

# Release the reservation to GPIO control line
request.release()
