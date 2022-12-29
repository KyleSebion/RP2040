from machine import Pin, PWM, ADC
import utime
led = Pin(25, Pin.OUT)

avg = 65535
N = 30

adc = ADC(Pin(27))

pwm = PWM(Pin(26))
pwm.freq(30000)
duty = 1000
pwm.duty_u16(duty)


while True:
    avg -= avg // N
    avg += adc.read_u16() // N
    #print(duty)
    if 15500 - avg > 0:
        duty = max(duty - 1, 0)
    else:
        duty = min(duty + 1, 65535)
        
    pwm.duty_u16(duty)
    #led.toggle()
    #utime.sleep_ms(5)
