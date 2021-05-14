from machine import *
from rp2 import *
from utime import *
import time
    
preamble = [9000, 4500]
period1 = 560
period2 = period1 * 3
b0 = [period1, period1]
b1 = [period1, period2]
end = [period1]
bits = { '0': b0, '1': b1 }
inv = { '0': '1', '1': '0' }
    
def getBinWithInv(byteVal):
    byteValB = '{0:08b}'.format(byteVal)
    return list(byteValB) + [ inv[c] for c in byteValB ]

def getPulses(byteAddr, byteCmd):
    addrB = getBinWithInv(byteAddr)
    cmdB = getBinWithInv(byteCmd)
    return None
    
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, out_init=rp2.PIO.OUT_LOW, autopull=True, pull_thresh=32, out_shiftdir=rp2.PIO.SHIFT_RIGHT)
def blink2():
    set(y, 1)
    label('part562')
    set(x, 20)
    label('pwm')
    mov(pins, y) [17]
    set(pins, 0) [16]
    jmp(x_dec, 'pwm')
    jmp(y_dec, 'part562')
    
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, out_init=rp2.PIO.OUT_LOW, autopull=True, pull_thresh=32, out_shiftdir=rp2.PIO.SHIFT_RIGHT)
def blink3():
    #pwm
    set(pins, 1) [16]
    set(x, 20)
    label('pwm')
    set(pins, 0) [17]
    set(pins, 1) [16]
    jmp(x_dec, 'pwm')
    #21.5 pwm cycles done
    
    set(pins, 0) [16]
    set(x, 20)
    label('sil')
    set(pins, 0) [17]
    set(pins, 0) [16]
    jmp(x_dec, 'sil')
    #43 pwm cycles done
    
    
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, out_init=rp2.PIO.OUT_LOW, autopull=True, pull_thresh=32, out_shiftdir=rp2.PIO.SHIFT_RIGHT)
def blink4():
    set(x, 0b01010)
    in_(x, 5)
    set(x, 0b10111)
    in_(x, 5)
    mov(x, isr)
    #pwm
    set(pins, 1) [16]
    label('pwm')
    set(pins, 0) [17]
    set(pins, 1) [16]
    jmp(x_dec, 'pwm')
    #21.5 pwm cycles done
    
    set(pins, 0) [16]
    set(x, 20)
    label('sil')
    set(pins, 0) [17]
    set(pins, 0) [16]
    jmp(x_dec, 'sil')
    #43 pwm cycles done

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, out_init=rp2.PIO.OUT_LOW, autopull=True, pull_thresh=32, out_shiftdir=rp2.PIO.SHIFT_RIGHT)
def blink22_21():
    set(pins, 1) [17]
    set(pins, 0) [16]
    set(x, 19)
    label('loop1')
    set(pins, 1) [17]
    set(pins, 0) [16]
    jmp(x_dec, 'loop1')
    set(pins, 1) [17]
    set(pins, 0) [17]
    
    set(pins, 0) [17]
    set(pins, 0) [16]
    set(x, 18)
    label('loop2')
    set(pins, 0) [17]
    set(pins, 0) [16]
    jmp(x_dec, 'loop2')
    set(pins, 0) [17]
    set(pins, 0) [17]
    

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, autopull=True, out_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_RIGHT)
def blink5():
    set(pins, 1) [31]
    set(x, 0b01010)
    in_(x, 5)
    set(x, 0b10111)
    in_(x, 5)
    mov(x, isr)
    set(y, 31)
    in_(y, 25)
    in_(x, 32)
    set(pins, 0) [31]
    nop() [5]
    
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, out_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_RIGHT)
def blink6():
    wrap_target()
    #get 32-bit command
    pull()                          #0
    
    label('handlebit')
    #set off loops parameter
    out(y, 1)[1]                    #1
    jmp(not_y, 'bit0')              #2
    
    label('bit1')
    #43 + 21 = 64
    #64 - 1 = 63 and 35 free cycles (starting at return address)
    mov(isr, null)                  #3
    set(y, 0b00001)                 #4
    in_(y, 5)                       #5
    set(y, 0b11110)                 #6
    in_(y, 5)                       #7
    mov(y, isr)                     #8
    jmp('endbit')                   #9
    
    label('bit0')
    #43 - 22 = 21
    #21 - 1 = 20 and 35 free cycles (starting at return address)
    set(y, 19) [6]                  #10
    label('endbit')
    
    #set return
    set(x, 15)                      #11
    mov(isr, x)                     #12
    
    #set square wave loops parameter
    set(x, 21)                      #13
    
    #call "function"
    jmp('signal')                   #14
    jmp(not_osre, 'handlebit') [21] #15
    
    set(x, 21)
    label('lastsquare')
    set(pins, 1) [17]
    set(pins, 0) [16]
    jmp(x_dec, 'lastsquare')
    wrap()
    
    #padding (things don't work right when instruction memory isn't full)
    nop()
    nop()
    nop()
    nop()
    nop()
    
    label('signal')
    
    label('square')
    set(pins, 1) [17]
    set(pins, 0) [16]
    jmp(x_dec, 'square')
    
    label('off')
    set(pins, 0) [17]
    set(pins, 0) [16]
    jmp(y_dec, 'off')
    
    mov(pc, isr)
    
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, out_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_RIGHT)
def blink():
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

def irqh(p):
    global i
    i += 1

led = Pin(25, Pin.OUT)
led.value(1)
    
sm = StateMachine(0, blink, freq=1376000, out_base=Pin(0), set_base=Pin(0))
i = 0
#sm.irq(irqh)
#print(sm.get())
#print(sm.get())
#print(sm.get())
sm.put(0b_01010010_10101101_11111111_00000000)
sm.put(0b_01010010_10101101_11111111_00000000)
sm.put(0b_01010010_10101101_11111111_00000000)
sm.put(0b_01010010_10101101_11111111_00000000)
sm.active(1)
sleep(1)
sm.active(0)
led.value(0)
