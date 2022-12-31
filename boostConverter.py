from machine import Pin, PWM, ADC
import utime
led = Pin(25, Pin.OUT)
avg = 65535
N = 30

adc = ADC(Pin(27))

pwm = PWM(Pin(26))
pwm.freq(80000)
duty = 0
pwm.duty_u16(duty)


while True:
    avg -= avg // N
    avg += adc.read_u16() // N
    #print(avg)
    if 40500 - avg > 0:
        duty = min(duty + 1, 65535 * 8 // 10)
    else:
        duty = max(duty - 1, 65535 * 1 // 10)
        
    pwm.duty_u16(duty)
    #led.toggle()
    #utime.sleep_ms(5)
