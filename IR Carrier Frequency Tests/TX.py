from machine import Pin
import uasyncio as asyncio
from ir_tx.nec import NEC

indicator_led = Pin("LED", Pin.OUT)

FREQ_36 = 36_000
FREQ_38 = 38_000 # Default
FREQ_40 = 40_000
FREQ_56 = 56_000

# Define an asynchronous function to handle IR transmission
async def repeat_tx(Freq=FREQ_38, Tx_Delay=3.0, Addr=0x01):
  ir_transmitter = NEC(Pin(17, Pin.OUT, value=0), freq=Freq) # Initialize IR transmitter on Pin 17
  commands = [0x01, 0xFF, 0x03, 0xFF, 0x08, 0x09, 0xA] # List of commands to send
  while True:
   for command in commands:
    ir_transmitter.transmit(Addr, command) # Send each command
    indicator_led.toggle()
    print(f"IR signal transmitted: Addr 0x{Addr:02x}, Command 0x{command:02x}")
    await asyncio.sleep(Tx_Delay) # Wait before sending the next command

# Main function to run the transmitter
async def main():
  await repeat_tx() # Call the transmit function

if __name__ == "__main__":
    print("Start Asyncio Main()")
    asyncio.run(main()) # Start the asynchronous event loop