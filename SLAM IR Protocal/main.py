from machine import Pin
from time import sleep

# For hardware testing
# if both are false, it will simulate tx/rx by directly injecting and extracting a tx block 
AUTOMATIC_TX = False
AUTOMATIC_RX = True

pin_Tx_test = Pin(6,Pin.IN,Pin.PULL_UP)
txPin = Pin(19, Pin.OUT)
rxPin = Pin(18, Pin.IN)

if AUTOMATIC_TX:
    import ir_tx.test as tx
    from ir_tx.slam import SLAM as tx_SLAM

    TX = tx_SLAM(txPin)
    tx.printSummery(TX)

    tx.main(TX)
elif AUTOMATIC_RX:
    import ir_rx.test as rx
    from ir_rx.slam import SLAM as rx_SLAM
    from ir_rx.print_error import print_error

    RX = rx_SLAM(rxPin, rx.callback)
    RX.error_function(print_error)
    rx.printSummery(RX)

    while True:
        sleep(0.1)
else:
    import ir_tx.test as tx
    from ir_tx.slam import SLAM as tx_SLAM

    import ir_rx.test as rx
    from ir_rx.slam import SLAM as rx_SLAM
    from ir_rx.print_error import print_error

    TX = tx_SLAM(txPin)
    RX = rx_SLAM(rxPin, rx.callback)
    RX.error_function(print_error)
    tx.printSummery(TX)
    rx.printSummery(RX)
    print("\nRunning Software Test")

    print("-Good Data Test. Expect Address: 0x2, Cmd 0xF")
    TX.transmit(0x02,0xF)
    txBlock = TX._arr
    rx.runTest(txBlock, RX)

# def CheckArray(arr):
#     total = 0
#     for _ in arr:
#         total += int(_)
#     return total


# print("Good Data Test. Expect Address: 0x5, Cmd 0xF")
# runTest(DataStream)

# print("Bad Data: Missing end")
# BadDataStream=DataStream[:]
# BadDataStream.append(100)
# runTest(BadDataStream)

# print("Bad Data: Flipped Bit")
# BadDataStream=DataStream[:]
# BadDataStream[5] = 1687
# runTest(BadDataStream)

# # print(f"Array of edge times: {slam_test._times}")
# # print(f"Number of edges: {slam_test.edge}")
# # print(f"Size of start block: {ticks_diff(slam_test._times[2],slam_test._times[1])}")