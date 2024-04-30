from machine import Pin
from time import sleep_ms
from ir_tx.slam import SLAM
# from ir_tx.nec import NEC
import constants

Addr = constants.ADDRESS

ir_transmitter = SLAM(Pin(constants.PIN_TX, Pin.OUT, value=0), freq=constants.FREQ) # Initialize IR transmitter on Pin 17
print(f"IR Tx initialized. Pin: {constants.PIN_TX}, Freq: {constants.FREQ} Hz, Address: {constants.ADDRESS}")

def transmit(command:int, Repeat_Delay=None):
  ir_transmitter.transmit(Addr, command)
  # print(f"IR signal transmitted: Addr 0x{Addr:01x}, Command 0x{command:02x}")
  if Repeat_Delay is not None:
    sleep_ms(Repeat_Delay) # Wait before repeating the transmission. Use this when you 
    ir_transmitter.transmit(Addr,command)

# Main function to run the transmitter
def main():
  pass # Call the transmit function

if __name__ == "__main__":
    print("Start Asyncio Main()")
    main() # Start the asynchronous event loop