from machine import Pin, PWM, ADC
import utime
led = Pin("LED", Pin.OUT)
avg = 65535
N = 30

adc = ADC(Pin(26))

pwm = PWM(Pin(27))
pwm.freq(30000)
pwm.duty_u16(0)
duty = 0


while True:
    avg -= avg // N
    avg += adc.read_u16() // N
    #print(avg)
    if 15500 - avg > 0:
        duty = min(duty + 1, 65535)
    else:
        duty = max(duty - 1, 0)
        
    pwm.duty_u16(duty)
    #led.toggle()
    #utime.sleep_ms(5)