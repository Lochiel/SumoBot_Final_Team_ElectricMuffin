from machine import Pin, Timer
import time

# Constants
SOUND_SPEED = 0.0343  # Speed of sound in cm/us
PULSE_DURATION = 10   # Duration of the pulse in microseconds

# Define the trigger and echo pins
trigger_pin = Pin(15, Pin.OUT)
echo_pin = Pin(14, Pin.IN)

def measure_distance():
    trigger_pin.low()
    time.sleep_us(2)
    trigger_pin.high()
    time.sleep_us(PULSE_DURATION)
    trigger_pin.low()
    
    # Measure the duration of pulse back
    timeout = 25000  # Timeout in microseconds, adjust as necessary
    start_time = time.ticks_us()

    while echo_pin.value() == 0:
        if time.ticks_diff(time.ticks_us(), start_time) > timeout:
            return None  # Return None if timeout
    signal_off = time.ticks_us()

    while echo_pin.value() == 1:
        if time.ticks_diff(time.ticks_us(), start_time) > timeout:
            return None  # Return None if timeout
    signal_on = time.ticks_us()
    
    time_passed = int(signal_on) - int(signal_off)
    distance = (time_passed * SOUND_SPEED) / 2  # Calculate distance in cm
    
    return distance

def check_distance():
    distance = measure_distance()
    if distance is None:
        print("No Echo received. Check sensor connections.")
    elif 0 < distance <= 20:
        print("Measured Distance:", distance, "cm")
        print("Positive feedback: program motors to turn SumoBot 180°")
    elif 21 <= distance <= 400:
        print("Measured Distance:", distance, "cm")
        print("Negative feedback: do nothing")
    else:
        print("Distance out of range")

while True:
    check_distance()
    time.sleep(1)  # Check the distance every 1 second
