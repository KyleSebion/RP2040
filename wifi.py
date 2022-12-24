import network
import utime
from machine import Pin
import usys
import ntptime
import time
import urequests
led = Pin('LED', Pin.OUT)
led.on()

print(time.localtime())

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
#print(wlan.scan())
wlan.connect('ssid', 'password')

deadline = utime.ticks_add(utime.ticks_ms(), 2000)
while not wlan.isconnected():
    print("connecting...")
    if utime.ticks_diff(deadline, utime.ticks_ms()) <= 0:
        print('failed to connect to wifi')
        usys.exit(1)
    utime.sleep_ms(100)
ntptime.settime() # seems to always be utc rather than +8
print(wlan.ifconfig())
print(time.localtime())
urequests.post('https://webhook.site/14726118-efc5-484f-8d3e-2192fdc29a0b', json='{}')
led.off()