# Team 2, 2440 Spring '24
# Cam Chalmers, Melissa Chavez, Anusha V
# # Adapted from code by Kiran Jojare

from machine import I2C, Pin
import seesaw
import time
import tx
from constants import command_codes
import uasyncio as asyncio

led = Pin("LED", Pin.OUT)

# Initialize I2C. Adjust pin numbers based on your Pico's configuration
# SCL = Yellow Wire, SDA = Blue Wire
i2c = I2C(0, scl=Pin(17), sda=Pin(16))

# Initialize the Seesaw driver with the I2C interface
# Use the Gamepad QT's I2C address from the Arduino code (0x50)
seesaw_device = seesaw.Seesaw(i2c, addr=0x50)

# Define button and joystick pin numbers as per the Arduino code
BUTTON_A = 5
BUTTON_B = 1
BUTTON_X = 6
BUTTON_Y = 2
BUTTON_START = 16
BUTTON_SELECT = 0
JOYSTICK_X_PIN = 14
JOYSTICK_Y_PIN = 15

# Button mask based on Arduino code
BUTTONS_MASK = (1 << BUTTON_X) | (1 << BUTTON_Y) | \
              (1 << BUTTON_A) | (1 << BUTTON_B) | \
              (1 << BUTTON_SELECT) | (1 << BUTTON_START)

# Initialize button states
button_states = {
   BUTTON_A: True,
   BUTTON_B: True,
   BUTTON_X: True,
   BUTTON_Y: True,
   BUTTON_START: True,
   BUTTON_SELECT: True
}

def setup_buttons():
   """Configure the pin modes for buttons."""
   seesaw_device.pin_mode_bulk(BUTTONS_MASK, seesaw_device.INPUT_PULLUP)

def read_buttons():
   """Read and return the state of each button."""
   return seesaw_device.digital_read_bulk(BUTTONS_MASK)

def process_buttons(current_buttons):
    """Returns tuple of the button states"""
    # current_buttons is a binary string, where each position indicates a different button
    # 1<<X creates a binary string with a 1 only in the location for a specific button
    # & compares the strings, and returns zero if there is no match, or non-zero if there is a match
    # in Python, any non-zero value evaluats to TRUE

    btn_A = not(bool(current_buttons & (1<<BUTTON_A)))
    btn_B = not(bool(current_buttons & (1<<BUTTON_B)))
    btn_X = not(bool(current_buttons & (1<<BUTTON_X)))
    btn_Y = not(bool(current_buttons & (1<<BUTTON_Y)))
    btn_Start = not(bool(current_buttons & (1<<BUTTON_START)))
    btn_Select = not(bool(current_buttons & (1<<BUTTON_SELECT)))

    return (btn_A, btn_B, btn_X, btn_Y, btn_Select, btn_Start)

##############
def transmit(code):
    # time.sleep_ms(constants.TX_DELAY)  # Delay to prevent overwhelming the output
    if code is not "STOP":
        print(f"Transmitting {command_codes[code]}")
    tx.transmit(command_codes[code].code)
    led.toggle()


#############

##  |---Deadzone---|            |---Middle--|                   |---Max---|
#   | deadzone > position       | middle > position > deadzone  | position > middle
#   | Do Nothing, output STOP   | Output SLOW                   | Output FAST

# How many ms between analog joystick reads?
GAMEPAD_READ_DELAY = 200

# Initialize joystick center position
joystick_center_x = 511
joystick_center_y = 497

#deadzon
joystick_deadzone_x = 50
joystick_deadzone_y = 50

#distance from  center
joystick_middle_x = 480
joystick_middle_y = 480

def joystick_absolute_values(position, center, dead, middle):
    """Returns the joysticks distance from center"""
    #get distance from center
    distance = abs(position - center)

    #translate that into 0,1,2
    value = 0
    if (distance > dead):
        if (distance < middle):
            value = 1
        elif (distance >= middle):
            value = 2
    else:
        value = 0
    
    # set the sign for left/right
    # Negative = left
    if (position - center) > 0:
        value = value * -1
    
    return value

def joystick_status(current_x, current_y):
    # Returns tuple (x,y)
    # x,y = 0,1,2 for joystick distance. 0 = centered, 1=moderate, 2 = full
    # Negative values indicate left/down
    
    # Translate into simplifed values
    x_value = joystick_absolute_values(current_x, joystick_center_x, joystick_deadzone_x, joystick_middle_x)
    y_value = joystick_absolute_values(current_y, joystick_center_y, joystick_deadzone_y, joystick_middle_y)

    return (x_value,y_value)

#################################

def main():
   """Main program loop."""

   setup_buttons()
   
   gamepad_lastread_tick = time.ticks_ms()

   while True:
        if (time.ticks_diff(time.ticks_ms(), gamepad_lastread_tick) > GAMEPAD_READ_DELAY):
            gamepad_lastread_tick = time.ticks_ms()


###### Buttons
            current_buttons = read_buttons()
            btn_A, btn_B, btn_X, btn_Y, btn_Select, btn_Start = process_buttons(current_buttons)
            turbo = btn_A

###### Joystick  
            # Read joystick values
            absolute_x = seesaw_device.analog_read(JOYSTICK_X_PIN)
            absolute_y = seesaw_device.analog_read(JOYSTICK_Y_PIN)

            current_x, current_y = joystick_status(absolute_x, absolute_y)

###### Command Priority order for Transmission
# - Turbo
# - Full direction
# - CW/CCW
# - Fwd/Rev
# - Sensor Toggle
# - NeoPixel Mode


            if (turbo) & (current_y ==2):
                transmit("FWD_TURBO")
            elif (turbo) & (current_y == -2):
                transmit("180")
            elif (turbo) & (current_x == 2):
                transmit("CW_DODGE")
            elif (turbo) & (current_x == -2):
                transmit("CCW_DODGE")

            elif (current_x == 2):
                transmit("CW_FAST")
            elif (current_x == -2):
                transmit("CCW_FAST")
            elif (current_y == 2):
                transmit("FWD_FAST")

            elif (current_x == 1):
                transmit("CW_SLOW")
            elif (current_x == -1):
                transmit("CCW_SLOW")

            elif (current_y == 1):
                transmit("FWD_SLOW")
            elif (current_y == -1) or (current_y == -2):
                transmit("REV")
            
            elif (btn_Start) or (btn_Select):
                transmit("SEN_BACK")
            elif (btn_B):
                transmit("NP_3")
            elif (btn_X):
                transmit("NP_2")
            elif (btn_Y):
                transmit("NP_1")
            
            else:
                transmit("STOP")


if __name__ == "__main__":
   GAMEPAD_READ_DELAY = 500
   main()
