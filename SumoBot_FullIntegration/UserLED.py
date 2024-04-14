from machine import Pin
import uasyncio as asyncio

FAST_BLINK = 500 #If a new on is sent while 
SLOW_BLINK = 1000

class LED:

    status = True

    def __init__(self, pin:Pin) -> None:
        self.pin = pin
    
    async def toggle(self) -> None:
        if self.status:
            await self._blink()
        else:
            self.pin.value(1)
            status = True


    
    async def _off(self):
        self.pin.value(0)

    async def _blink(self):
        self.pin.value(0)
        await asyncio.sleep_ms(FAST_BLINK)
        self.pin.value(1)

