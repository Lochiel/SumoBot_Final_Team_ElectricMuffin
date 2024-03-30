import ir_tx

from machine import Pin
import uasyncio as asyncio
from ir_tx.nec import NEC

indicator_led = Pin("LED", Pin.OUT)

TEST36 = 36_000
TEST38 = 38_000 # Default
TEST40 = 40_000
TEST56 = 56_000


# Define an asynchronous function to handle IR transmission
async def transmit_ir(Freq=TEST38, Tx_Delay=3, Addr=0x01):
  ir_transmitter = NEC(Pin(17, Pin.OUT, value=0), freq=Freq) # Initialize IR transmitter on Pin 17
  commands = [0xa1, 0xa2, 0xa0, 0xb1, 0xb2, 0xb0] # List of commands to send

  while True:
   for command in commands:
    ir_transmitter.transmit(Addr, command) # Send each command
    indicator_led.toggle()
    print(f"IR signal transmitted: Addr {Addr}, Command {command}")
    await asyncio.sleep(Tx_Delay) # Wait before sending the next command

# Main function to run the transmitter
async def main(Jamming=False, Freq=TEST38, Delay=None):

  if Jamming:
    Tx_Delay = Delay or 0.3
    Addr = 0xAF # Jamming device address
    await asyncio.sleep(0.1)
  else: 
    Tx_Delay = Delay or 3
    Addr = 0x01 # Non-Jamming device address
  print("Start TX Main(): JAMMING: ",Jamming," FREQ: ",Freq, " Tx Delay: ", Tx_Delay)
  await transmit_ir(Freq, Tx_Delay, Addr) # Call the transmit function


print("Start")
if __name__ == "__main__":
    print("Start Asyncio Main()")
    asyncio.run(main()) # Start the asynchronous event loop