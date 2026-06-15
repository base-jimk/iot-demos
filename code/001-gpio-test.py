import time
import gpiod

chip = gpiod.Chip("/dev/gpiochip0")

#led_line = chip.get_line(17)

request = chip.request_lines(
	consumer="test",
	config={
		17:gpiod.LineSettings(direction=gpiod.line.Direction.OUTPUT)
		}
)

print("LED ON")
request.set_value(17,gpiod.line.Value.ACTIVE
)

time.sleep(5)

print("LED OFF")
request.set_value(17,gpiod.line.Value.INACTIVE)

request.release()
