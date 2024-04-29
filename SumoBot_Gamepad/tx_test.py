import constants
from machine import Pin
from time import sleep, sleep_ms
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
                sleep_ms(200)

if __name__ == "__main__":
    main()
    