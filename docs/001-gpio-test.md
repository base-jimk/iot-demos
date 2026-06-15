# Project 001: RPi 5 GPIO Test 
#### Objective: Test the On/Off functionality of Raspberry Pi General Pupose I/O Pins
#### Related code: 001-gpio-test.py
#### Last Update: 15JUN2026
## Equipment:
* Raspberry Pi 5 
* Discrete electronic component (e.g. LED) 
## Software Dependencies:
* Raspberry Pi OS Debian v13.5 "Trixie"
* libgpiod v2.2.1 (included with Trixie)
## Write-Up
So you have a brand new RPi 5 and want to start testing it out. Testing the functionality of the 3.3V GPIO pins is a great place to start. 

Testing GPIO functionality is non-trivial on RPi 5 for two reasons. For one, the "Trixie" version of Debian (v13) no longer pre-installs the [pigpio daemon](https://abyz.me.uk/rpi/pigpio/pigpiod.html) for controlling GPIO interfaces. This daemon was used in previous RPi OS versions, and also is required by the commonly used [gpiozero library](https://gpiozero.readthedocs.io/en/stable/) for GPIO pin control. We'll use [libgpiod](https://libgpiod.readthedocs.io/en/master/), an alternative library that supports newer GPIO interfaces (introduced in Linux kernel v4.8) and comes pre-installed with Trixie. 

A second snag is that RPi 5 has a different hardware architecture for addressing its GPIO chips from previous board versions. The RPi board uses GPIO extender chips to increase the number of pins controlled by the SoC. You can see a list of your GPIO chips using the `gpiodetect` command. RPi 5 initially used `gpiochip4` for user-facing control of GPIO lines, but this was changed via a Linux kernel update in July 2024 to `gpiochip0` (see this [whitepaper](https://pip-assets.raspberrypi.com/categories/685-whitepapers-app-notes/documents/RP-006553-WP/A-history-of-GPIO-usage-on-Raspberry-Pi-devices-and-current-best-practices) for the full details). Here's what you should see with the `gpiodetect` command in ternimal:
```
    pi@pi5:~ $ gpiodetect
    gpiochip0 [pinctrl-rp1] (54 lines)          <-- This is the chip we want
    gpiochip10 [gpio-brcmstb@107d508500] (32 lines)
    gpiochip11 [gpio-brcmstb@107d508520] (4 lines)
    gpiochip12 [gpio-brcmstb@107d517c00] (17 lines)
    gpiochip13 [gpio-brcmstb@107d517c20] (6 lines)
```
If the `[pinctrl-rpl] (54 lines)` is associated with `gpiochip4` on your RPi, you will need to change the corresponding line of code in 001-gpio-test.py to match: 
`chip=gpiod.Chip("dev/gpiochip4")`

With those technical details squared away, we can get started. Connect a discrete electronic component (like an LED) to pin #17 of the GPIO 3.3V pins, or any pin you prefer; see RPi5 pinout here: https://pinout.xyz/pinout/. Connect to your RPi (I will use SSH from my main computer), create a project directory, and copy 001-gpio-test.py into your directory. One method to copy a file's contents from GitHub to a local file is using `curl -o [output filename] [github raw URL for file]` 

Modify the `gpioPin` variable accordingly if you are using a different pin than pin 17, and use `python3 001-gpio-test.py` to run. The code has line-level comments so you can see what each line is doing. Your LED should turn on for 5 seconds and then turn back off before the program terminates!

## Troubleshooting
If you receive a `PermissionError: [Errno 13] Permission denied` error when attempting to run the .py file, then the user profile you are using to run the code probably doesn't have permissions to the gpio group. You can fix this with `sudo usermod -aG gpio $USER` and logging out/back in or rebooting your RPi.

You can also work around this issue by running the python3 command as `sudo` or from a root user account, but consider following the principle of least privileges for security reasons. 
