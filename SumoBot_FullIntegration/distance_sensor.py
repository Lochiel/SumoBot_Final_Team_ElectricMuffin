from machine import Pin, Timer
import time
import constants

SOUND_SPEED = 0.0343  # in cm./us.
PULSE_DURATION = 10   # in us.

trigger_pin = Pin(constants.PIN_SENSOR_TRIGGER, Pin.OUT)
echo_pin = Pin(constants.PIN_SENSOR_RETURN, Pin.IN)

def measure_distance():
    trigger_pin.low()
    time.sleep_us(2)
    trigger_pin.high()
    time.sleep_us(PULSE_DURATION)
    trigger_pin.low()
    
    timeout = 25000  
    start_time = time.ticks_us()   

    while echo_pin.value() == 0:
        if time.ticks_diff(time.ticks_us(), start_time) > timeout:
            return None  
    signal_off = time.ticks_us()

    while echo_pin.value() == 1:
        if time.ticks_diff(time.ticks_us(), start_time) > timeout:
            return None 
    signal_on = time.ticks_us()
    
    time_passed = int(signal_on) - int(signal_off)
    distance = (time_passed * SOUND_SPEED) / 2  # in cm.
    
    return distance

def check_distance():
    distance = measure_distance()
    if distance is None:
        # print("check sensor connections (no echo recieved)")
        return False
    elif 0 < distance <= 20:
        # print("Measured Distance:", distance, "cm")
        print("turn 180° !!")
        return True
    elif 21 <= distance <= 400:
        # print("Measured Distance:", distance, "cm")
        # print("do nothing")
        return False
    else:
        # print("out of range")
        return False


if __name__ == '__main__':
    while True:
        check_distance()
        time.sleep(1)  # check distance every 1 second
