import uasyncio as asyncio

# Role = "Jammer" #Jammer Sender Reciever
Role = "Sender"
# Role = "Reciever"

if Role == "Jammer":
    import TX
    Freq=       TX.FREQ_38
    Tx_Delay=   0.3
    Addr=       0xAF
elif Role == "Sender":
    import TX
    Freq=       TX.FREQ_38
    Tx_Delay=   2
    Addr=       0x5
else:
    import RX

if Role in {"Jammer", "Sender"}:
    print(f"Start TX: {Role} FREQ: {Freq} Tx Delay: {Tx_Delay} Addr: 0x{Addr:02X}")
    asyncio.run(TX.repeat_tx(Freq=Freq, Tx_Delay=Tx_Delay, Addr=Addr))
else:
    print("Start Rx waiting loop. Addr: ",RX.address)

# Asynchronous main loop to keep the script running
async def main():
  while True:
    await asyncio.sleep_ms(100) # Sleep for 100 ms

if __name__ == "__main__":
    asyncio.run(main()) # Start the asynchronous event loop