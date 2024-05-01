from slam import SLAM
from machine import Pin
from time import sleep

FREQ_36 = 36_000
FREQ_38 = 38_000 # Default
FREQ_40 = 40_000
FREQ_56 = 56_000

led = Pin("LED", Pin.OUT)
pin_Tx_test = Pin(6,Pin.IN,Pin.PULL_UP)

def Tx_test_pin():
    return pin_Tx_test.value()

def TxTimeCalculation(input):
    packet_list = input
    tx_time = 0
    for _ in packet_list:
        tx_time += _
    return tx_time

def printSummery(tx):
    print("\n---TX Summery---")
    print(f"Dot: {tx._DOT}us")
    print(f"Dash: {tx._DASH}us")
    tx.transmit(0x2,0xF,None)
    tx_string = tx._arr
    print(f"Number of on/offs: {len(tx_string)} Tx Time: {TxTimeCalculation(tx_string)}us")
    print(f"(TX: {tx_string}")

def main(tx):
    print("Starting RX test. Use ")
    while True:
        if Tx_test_pin():
            sleep(0.1)
        for addr in range(0,0xF+1):
            if Tx_test_pin():
                break
            for data in range(0,0xF+1):
                print(f"Tx addr: {addr} data: {data}")
                tx.transmit(addr,data)
                led.toggle()
                sleep(0.2)
                if Tx_test_pin():
                    print("Stopping due to input")
                    break

if __name__ == "__main__":
    pin = Pin(19, Pin.OUT)
    tx = SLAM(pin)
    printSummery(tx)
    main(tx)
