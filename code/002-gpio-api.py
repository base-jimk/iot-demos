from contextlib import asynccontextmanager #context manager, used to guarantee cleanup

import gpiod
from fastapi import FastAPI
from fastapi import Request

@asynccontextmanager
# describes the setup (request GPIO ownership) > yield (handle GPIO) > close (release)	chip
async def lifespan(app: FastAPI):
	chip = gpiod.Chip("/dev/gpiochip0")  #use gpioinfo to check which has IO; chip mapping non-intuitive
	led_line = chip.request_lines(
		consumer="fastapi-led",
		config={
			17: gpiod.LineSettings(direction=gpiod.line.Direction.OUTPUT)
			}
		)
	# App States (globals)
	app.state.chip = chip
	app.state.led_line = led_line
	app.state.initialized = True
	app.state.led_status = "off"

	yield

	print("Releasing GPIO Lines...")
	led_line.set_value(17, gpiod.line.Value.INACTIVE)
	led_line.release()
	chip.close()
	app.state.initialized = False

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
	return {"message": "FastAPI GPIO Demo!"}

@app.post("/led/on")
# request: Request - states that "request" is expected datatype 'Request'
# request must pass from app  > state to hit the GPIO line resource
# the 'Request' object is a dict-like object that itemizes the HTTP request
def led_on(request: Request):
	request.app.state.led_line.set_value(17,gpiod.line.Value.ACTIVE)
	app.state.led_status = "on"
	return {"status": app.state.led_status}

@app.post("/led/off")
def led_off(request: Request):
	request.app.state.led_line.set_value(17,gpiod.line.Value.INACTIVE)
	app.state.led_status = "off"
	return {"status":app.state.led_status}

@app.get("/status")
def get_status():
	return  {
		"initialized": app.state.initialized,
		"led": app.state.led_status
		}
