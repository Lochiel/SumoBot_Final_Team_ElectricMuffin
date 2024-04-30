from machine import Pin
import uasyncio as asyncio
from ir_tx.nec import NEC
import constants

Addr = constants.ADDRESS

ir_transmitter = NEC(Pin(constants.PIN_TX, Pin.OUT, value=0), freq=constants.FREQ) # Initialize IR transmitter on Pin 17
print(f"IR Tx initialized. Pin: {constants.PIN_TX}, Freq: {constants.FREQ} Hz, Address: {constants.ADDRESS}")

async def transmit(command:int, Tx_Delay=constants.TX_DELAY):
  ir_transmitter.transmit(Addr, command)
  # print(f"IR signal transmitted: Addr 0x{Addr:01x}, Command 0x{command:02x}")
  await asyncio.sleep_ms(Tx_Delay) # Wait before sending the next command    

# Main function to run the transmitter
async def main():
  pass # Call the transmit function

if __name__ == "__main__":
    print("Start Asyncio Main()")
    asyncio.run(main()) # Start the asynchronous event loop