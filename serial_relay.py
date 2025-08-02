from machine import Pin
from sys import stdin

LED_ON = 1
LED_OFF = 0
led = Pin(25, Pin.OUT)

RELAY_CLOSE = 0
RELAY_OPEN = 1
relay = Pin(16, Pin.OUT)

print("start")
while True:
    if not "line" in globals():
        line = "ON"
    else:
        line = stdin.readline().strip().upper()
    if line == "OFF":
        led.value(LED_OFF)
        relay.value(RELAY_OPEN)
        state = line
        print("relay: open; nc: open; no: closed; coil pwr: on; red relay led: on; green pico led: off")
    elif line == "ON":
        led.value(LED_ON)
        relay.value(RELAY_CLOSE)
        print("relay: closed; nc: closed; no: open; coil pwr: off; red relay led: off; green pico led: on")
        state = line
    elif line == "STATE":
        print("state: " + state)
    elif line == "REPL":
        print("REPL")
        break
    elif line == "":
        pass
    else:
        print(line + " is invalid. use: OFF|ON|STATE|REPL")
