from machine import Pin
from time import sleep

# For hardware testing
# if both are false, it will simulate tx/rx by directly injecting and extracting a tx block 
AUTOMATIC_TX = True
AUTOMATIC_RX = False

SLAM = False

pin_Tx_test = Pin(6,Pin.IN,Pin.PULL_UP)
txPin = Pin(19, Pin.OUT)
rxPin = Pin(18, Pin.IN)

if AUTOMATIC_TX:
    import ir_tx.test as tx_test
    if SLAM:
        from ir_tx.slam import SLAM as tx_SLAM
        TX = tx_SLAM(txPin)
        tx_test.printSummery(TX)
    else:
        from ir_tx.nec import NEC as tx_NEC
        TX = tx_NEC(txPin)
    tx_test.main(TX)

elif AUTOMATIC_RX:
    import ir_rx.test as rx_test
    if SLAM:
        from ir_rx.slam import SLAM as rx_SLAM
        RX = rx_SLAM(rxPin, rx_test.callback)
        rx_test.printSummery(RX)
    else:
        from ir_rx.nec import NEC_16 as rx_NEC
        RX = rx_NEC(rxPin, rx_test.callback)
    from ir_rx.print_error import print_error
    RX.error_function(print_error)

    while True:
        sleep(0.1)
else:
    import ir_tx.test as tx_test
    import ir_rx.test as rx_test
    if SLAM:
        from ir_tx.slam import SLAM as tx_SLAM
        from ir_rx.slam import SLAM as rx_SLAM

        TX = tx_SLAM(txPin)
        RX = rx_SLAM(rxPin, rx_test.callback)
    else:
        from ir_tx.nec import NEC as tx_NEC
        from ir_rx.nec import NEC_8 as rx_NEC

        TX = tx_NEC(txPin)
        RX = rx_NEC(txPin, rx_test.callback)

    from ir_rx.print_error import print_error

    RX.error_function(print_error)
    tx_test.printSummery(TX)
    rx_test.printSummery(RX)
    print("\nRunning Software Test")

    print("-Good Data Test. Expect Address: 0x2, Cmd 0xF")
    TX.transmit(0x02,0xF)
    txBlock = TX._arr
    rx_test.runTest(txBlock, RX)

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