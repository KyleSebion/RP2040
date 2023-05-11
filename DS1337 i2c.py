import utime
import binascii
from machine import Pin, Timer, I2C
led = Pin("LED", Pin.OUT)
timer = Timer()

def blink(timer):
    led.toggle()

timer.init(freq=20, mode=Timer.PERIODIC, callback=blink)

sda = machine.Pin(0)
scl = machine.Pin(1)
i2c = machine.I2C(0, sda=sda, scl=scl, freq=100000)
print(i2c.scan())
while True:
    utime.sleep(1)
    val = list(i2c.readfrom_mem(0x68, 0x0, 1))[0]
    s = (0b0001111 & val) + ((0b1110000 & val) >> 4) * 10
    
    val = list(i2c.readfrom_mem(0x68, 0x1, 1))[0]
    m = (0b0001111 & val) + ((0b1110000 & val) >> 4) * 10 
    print("{}:{}".format(m,s))
