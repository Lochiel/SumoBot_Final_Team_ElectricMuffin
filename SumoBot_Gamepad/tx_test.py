from SumoBot_FullIntegration import constants
from machine import Pin
import uasyncio as asyncio
import tx

print("Entering Test Mode")

led = Pin(constants.PIN_LED1, Pin.OUT, value=0)
codes = constants.command_codes

async def main():
    while True:
        for _ in codes:
            if "NP_" in _:
                led.toggle()
                await tx.transmit(codes[_].code)
                await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(main())