import ir_rx
from machine import Pin
from ir_rx.nec import NEC_8 # Use the NEC 8-bit class
from ir_rx.print_error import print_error # for debugging

led = Pin("LED", Pin.OUT)

# Callback function to execute when an IR code is received
def ir_callback(data, addr, _):
 if addr == 0x01:
   print(f"Received NEC command! Data: 0x{data:02X}, Addr: 0x{addr:02X}")
   led.toggle()
 else:
   print(f"Error. Received Addr: 0x{addr:02X}")

# Setup the IR receiver
ir_pin = Pin(16, Pin.IN, Pin.PULL_UP) # Adjust the pin number based on your wiring
ir_receiver = NEC_8(ir_pin, callback=ir_callback)

# Optional: Use the print_error function for debugging
ir_receiver.error_function(print_error)

# Main loop to keep the script running

if __name__ == "__main__":
   print("Starting Rx wait loop")
   while True:
      pass # Execution is interrupt-driven, so just keep the script alive
