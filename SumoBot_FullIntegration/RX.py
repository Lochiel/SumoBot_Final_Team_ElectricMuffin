from machine import Pin
from ir_rx.nec import NEC_8 # Use the NEC 8-bit class
from ir_rx.print_error import print_error # for debugging
import uasyncio as asyncio
# from collections.abc import Callable
import constants

class IR_RX:

  def __init__(self, pin:int, address:int, callback_function) -> None:
    self.address = address
    self.callback = callback_function

    # Setup the IR receiver
    self.ir_pin = Pin(pin, Pin.IN, Pin.PULL_UP) # Adjust the pin number based on your wiring
    self.ir_receiver = NEC_8(self.ir_pin, callback=self.ir_callback)

    self.ir_receiver.error_function(print_error) # Optional: Use the print_error function for debugging  
    pass

  # Callback function to execute when an IR code is received
  def ir_callback(self, data, addr, _):
    if self.address == addr:
      self.callback(data)
    else:
      print(f"Error. Received Addr: 0x{addr:02X}")

# Callback function to execute when an IR code is received
def _ir_callback_test(data, _):
    print(f"Received NEC command! Data: 0x{data:02X}")
 
# Main loop to keep the script running
if __name__ == "__main__":
   RX = IR_RX(constants.PIN_RX, constants.ADDRESS, _ir_callback_test)
   print("Starting Rx wait loop")
   while True:
      _ = asyncio.sleep_ms(100) # Sleep for 100 ms
      pass # Execution is interrupt-driven, so just keep the script alive
