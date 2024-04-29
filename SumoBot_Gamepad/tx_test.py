import constants
from machine import Pin
from time import sleep
import tx

print("Entering Test Mode")

led = Pin(constants.PIN_LED1, Pin.OUT, value=0)
codes = constants.command_codes

def main():
    while True:
        for _ in codes:
            if "NP_" in _:
                led.toggle()
                tx.transmit(codes[_].code)
                sleep(2)

if __name__ == "__main__":
    main()
    