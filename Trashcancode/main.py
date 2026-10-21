from machine import Pin, PWM
import time

# ===== LED =====
led = Pin("LED", Pin.OUT)
led.toggle() 

signal1 = Pin(16, Pin.IN, Pin.PULL_DOWN)  # PET  
signal2 = Pin(19, Pin.IN, Pin.PULL_DOWN)  # BURN  
signal3 = Pin(18, Pin.IN, Pin.PULL_DOWN)  # CAN  

servo1 = PWM(Pin(11))  # Lucka 1  x
servo2 = PWM(Pin(9))  # Lucka 2  y 
servo3 = PWM(Pin(13))  # Lucka 3  z
servo1.freq(50)
servo2.freq(50)
servo3.freq(50)

SERVO_OPEN_X_PET = 6767    #6767
SERVO_CLOSED_X_PET = 8400  # 8400 neråt

SERVO_OPEN_Y_BURN = 2300  # 2300
SERVO_CLOSED_Y_BURN = 4000 # 4000

SERVO_OPEN_Z_CAN = 6969 
SERVO_CLOSED_Z_CAN = 4800 

## X
# open 6767
# closed 8400

## Y
# open 2300
# closed 4000

## Z: Kort sida
# open 6969
# closed 4800


state1 = 0
state2 = 0
state3 = 0

def set_servo(servo, pos):
    servo.duty_u16(pos)

# Start stängda
set_servo(servo1, SERVO_CLOSED_X_PET)
set_servo(servo2, SERVO_CLOSED_Y_BURN)
set_servo(servo3, SERVO_CLOSED_Z_CAN)

print("Pico start - 2 luckor + LED1")

while True:
    sig1 = signal1.value()
    sig2 = signal2.value()
    sig3 = signal3.value()

    # Lucka 1
    if sig1 == 1 and state1 == 0:
        print("Öppnar lucka 1")
        set_servo(servo1, SERVO_OPEN_X_PET)
        state1 = 1

    elif sig1 == 0 and state1 == 1:
        print("Stänger lucka 1")
        set_servo(servo1, SERVO_CLOSED_X_PET)
        state1 = 0

    # Lucka 2
    if sig2 == 1 and state2 == 0:
        print("Öppnar lucka 2")
        set_servo(servo2, SERVO_OPEN_Y_BURN)
        state2 = 1

    elif sig2 == 0 and state2 == 1:
        print("Stänger lucka 2")
        set_servo(servo2, SERVO_CLOSED_Y_BURN)
        state2 = 0
        
        # Lucka 3
    if sig3 == 1 and state3 == 0:
        print("Öppnar lucka 3")
        set_servo(servo3, SERVO_OPEN_Z_CAN)
        state3 = 1

    elif sig3 == 0 and state3 == 1:
        print("Stänger lucka 3")
        set_servo(servo3, SERVO_CLOSED_Z_CAN)
        state3 = 0
    print(sig1, sig2, sig3)
    time.sleep(0.05)
