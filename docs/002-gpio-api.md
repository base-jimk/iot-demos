# Project 002: RESTful API For RPi GPIO Control
#### Objective: Use FastAPI to control RPi GPIO pins remotely via HTTP over a single network
* For connections outside a single network, a VPN (e.g. [Tailscale](https://tailscale.com/)) or Cloud Broker (e.g. [AWS IoT Core](https://aws.amazon.com/iot-core/)) is required. That will be a separate project!
#### Related code: 002-gpio-api.py
#### Last Update: 15JUN2026
## Equipment:
* Raspberry Pi 5 
* Discrete electronic component (e.g. LED) 
## Software Dependencies:
* Raspberry Pi OS Debian v13.5 "Trixie"
* gpiod-2.4.3 
* fastapi
* uvicorn
## Environment Setup
For initial setup, connect to your RPi, create a project folder, create and activate a virtual environment, and install dependcies using pip:
* `python -m venv .gpio-api`     _(create virtual environment named .gpio-api)_
* `source .gpio-api/bin/activate`   _(activate virtual environment)_
* `pip install gpiod`         _(install gpiod library)_
* `pip install fastapi` _(install fastapi)_
* `pip install uvicorn` _(install uvicorn)_

Alternatively, `pip install "fastapi[standard]"` installs both fastapi, uvicorn, and a more enhanced CLI, but I am just going to keep this light weight. 

When finished, `deactivate` closes the venv and then you can `rm rf` the venv folder if you want to get rid of it.

## Write-Up
This is a very simple script that handles three requests from clients:
* POST /led/on - Turn the LED on (GPIO pin Active)
* POST /led/off - Turn the LED off (GPIO pin Inactive)
* GET /status - Check if the LED is on or off

Looking at 002-gpio-api.py, it is similar to our first project (001-gpio-test.py), except that  we now have the gpio line setting commands wrapped inside of functions that trigger on HTTP requests. 

One significant difference is that we also added a lifespan function to manage the application lifecycle. Since the GPIO line needs to reserved in order to handle user commands, and released at shutdown to free the line for other applications, there is a Startup > Yield > Shutdown flow to the application that looks something like this:
* Startup - Request GPIO line
* Yield - Handle client requests on GPIO line (GET/POST) 
* Shutdown - Release GPIO line

Across the lifecycle, variables that are needed by multiple endpoints (API calls) are owned by `app.state`, which provides somewhat of a global scope for these variables.

To run this code, run the following command:  
`uvicorn 002-gpio-api:app --host 0.0.0.0 --port 8000`

This starts up a uvicorn web server that listens on a "socket" (IP Address + Port + Protocol), hands user requests over to FastAPI, and hands FastAPI's responses back to the user. Note that the `--host 0.0.0.0` segment tells uvicorn to listen to all network connections, either via wi-fi or ethernet.

The easiest way to test out your API in a web browser from another computer on the same network is with FastAPI's built in 'Swagger' user interface at `http://[YourPiAddress]:8000/docs`.  Click the 'Try it Out' and 'Execute' buttons for each request -- you'll know if it's working properly if response codes are 200 (Successful Response) for each request and the reponse body matches expected output (e.g. {"status": "off"}).

Alternatively, web browser address bars send GET requests, so you can access the root and /status methods with (respectively):  
`http://[YourPiAddress]:8000`   
`http://[YourPiAddress]:8000/status`

The web browser address bar doesn't allow you to send POST requests, so you'll need to use `curl` in order to send those requests over. JSON responses with the led {"status": } should return in your terminal:   
`curl -X POST http://[YourPiAddress]:8000/led/on`  
`curl -X POST http://[YourPiAddress]:8000/led/off`  

To summarize what we have accomplished:  
User/Client - HTTP request  
-> Uvicorn - Listens for requests, sends to FastAPI   
--> FastAPI - Matches HTTP method + URL to a route, parses request parameters, calls Python functions, provides app states  
---> Python function - Calls GPIOD methods  
----> GPIOD Methods - Calls Linux kernel GPIO driver to manipulate hardware  
---> Python function - Returns {"led":"on"} (or similar status)  
--> FastAPI - Converts dict to JSON  
-> Uvicorn - HTTP Response (200 OK)  
User/Client - Receives HTTP response




















