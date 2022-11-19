from machine import *
from rp2 import *
from utime import *
import time
import struct

def rotate(l, n):
    return l[n:] + l[:n]
    
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, out_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT)
def smproc():
    pull()
    set(x, 23)
    label('sbit')
    out(y, 1)
    jmp(not_y, 'bit0')
    
    label('bit1')
    set(pins, 1) [15]
    set(pins, 0) [4]
    jmp('ebit')
    
    label('bit0')
    set(pins, 1) [7]
    set(pins, 0) [12]
    jmp('ebit')
    
    label('ebit')
    jmp(x_dec, 'sbit')
    
    
arr = [0x00_FF_00_00,
       0x5A_FF_00_00,
       0xFF_FF_00_00,
       0xFF_00_00_00,
       0xFF_00_FF_00,
       0x00_00_FF_00,
       0x00_5A_FF_00,
       0x00_FF_FF_00,
       0x00_FF_00_00,
       0x5A_FF_00_00,
       0xFF_FF_00_00,
       0xFF_00_00_00,
       0xFF_00_FF_00,
       0x00_00_FF_00,
       0x00_5A_FF_00,
       0x00_FF_FF_00,
       0x00_FF_00_00,
       0x5A_FF_00_00,
       0xFF_FF_00_00,
       0xFF_00_00_00,
       0xFF_00_FF_00,
       0x00_00_FF_00,
       0x00_5A_FF_00,
       0x00_FF_FF_00,
       0x00_FF_00_00,
       0x5A_FF_00_00,
       0xFF_FF_00_00,
       0xFF_00_00_00,
       0xFF_00_FF_00,
       0x00_00_FF_00,
       0x00_5A_FF_00,
       0x00_FF_FF_00,
       0x00_FF_00_00,
       0x5A_FF_00_00,
       0xFF_FF_00_00,
       0xFF_00_00_00,
       0xFF_00_FF_00,
       0x00_00_FF_00,
       0x00_5A_FF_00,
       0x00_FF_FF_00,
       0x00_FF_00_00,
       0x5A_FF_00_00,
       0xFF_FF_00_00,
       0xFF_00_00_00,
       0xFF_00_FF_00,
       0x00_00_FF_00,
       0x00_5A_FF_00,
       0x00_FF_FF_00,
       0x00_FF_00_00,
       0x5A_FF_00_00,
       0xFF_FF_00_00,
       0xFF_00_00_00,
       0xFF_00_FF_00,
       0x00_00_FF_00,
       0x00_5A_FF_00,
       0x00_FF_FF_00,
       0x00_FF_00_00,
       0x5A_FF_00_00,
       0xFF_FF_00_00,
       0xFF_00_00_00,
       0xFF_00_FF_00,
       0x00_00_FF_00,
       0x00_5A_FF_00,
       0x00_FF_FF_00]

led = Pin(25, Pin.OUT)
led.value(1)
sm = StateMachine(0, smproc, freq=20000000, out_base=Pin(16), set_base=Pin(16))
sm.active(1)
#sm.put(0x00_FF_00_00) # GRB<Dummy>


while True:
    for i in range(len(arr)):
        sm.put(arr[i])
    arr = rotate(arr, 1)
    sleep(0.05)