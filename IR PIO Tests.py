from machine import *
from rp2 import *
from utime import *
import time
import struct
    
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, out_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT)
def handleNECIR():
    wrap_target()
    pull()
    
    mov(isr, null)
    set(x, 0b01010)
    in_(x, 5)
    set(x, 0b10111)
    in_(x, 5)
    mov(x, isr)
    label('squarepreamble')
    set(pins, 1) [17]
    set(pins, 0) [16]
    jmp(x_dec, 'squarepreamble')
    
    
    set(y, 5) [29]
    label('offpreamble')
    set(x, 31) [1]
    label('offpreamble2')
    jmp(x_dec, 'offpreamble2') [31]
    jmp(y_dec, 'offpreamble')
    
    label('handlebit')
    
    set(x, 21)
    label('squarebit')
    set(pins, 1) [17]
    set(pins, 0) [16]
    jmp(x_dec, 'squarebit')
    
    out(y, 1) [20]
    jmp(not_y, 'bit0') [31]
    label('bit1')
    #36 * 64 = 2304
    #43 + 21 = 64
    #64 - 1 = 63 and 35 free cycles
    set(x, 21) [16] #22 * 100 = 2200; 49 (from these instructions) + 21 (out) + 32 (top jmp) + 1 (last jmp) + 1 (top set x) = 104
    jmp('endbit') [31]
    label('bit0')
    #21 * 36 = 756
    #43 - 22 = 21
    #21 - 1 = 20 and 35 free cycles
    set(x, 6) # * 100 = 700; 1 (from these instructions) + 21 (out) + 32 (top jmp) + 1 (last jmp) + 1 (top set x) = 56
    label('endbit')
    label('offbit')
    nop() [31]
    nop() [31]
    nop() [31]
    jmp(x_dec, 'offbit') [3]
    
    jmp(not_osre, 'handlebit')
    
    set(x, 21)
    label('lastsquare')
    set(pins, 1) [17]
    set(pins, 0) [16]
    jmp(x_dec, 'lastsquare')
    wrap()
    
def getIR32Bit(byteAddr, byteCmd):
    return struct.unpack('>I', (struct.pack('BBBB', byteAddr, ~byteAddr, byteCmd, ~byteCmd)))[0]

led = Pin(25, Pin.OUT)
led.value(1)

#toggle on/off
p16 = Pin(16, Pin.IN, Pin.PULL_UP)
p16.irq(lambda pin: sm.put(getIR32Bit(0x20, 0x10)), Pin.IRQ_FALLING)

#turn off
p17 = Pin(17, Pin.IN, Pin.PULL_UP)
p17.irq(lambda pin: sm.put(getIR32Bit(0x20, 0xA3)), Pin.IRQ_FALLING)

#turn on
p18 = Pin(18, Pin.IN, Pin.PULL_UP)
p18.irq(lambda pin: sm.put(getIR32Bit(0x20, 0x23)), Pin.IRQ_FALLING)

sm = StateMachine(0, handleNECIR, freq=1376000, out_base=Pin(0), set_base=Pin(0))
sm.active(1)
while True:
    sleep(1)
sm.active(0)
led.value(0)
