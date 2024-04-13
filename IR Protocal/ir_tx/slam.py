# SumoBot Little Asynchronous Messaging - SLAM 
# Encoder for IR transmission of SumoBots
# Written by Cam Chalmers
# For ECEN 2440 - Applications of Embedded Systems, Spring '24
# Modified NEC code
# Based on code by Peter Hinch

#DONE Reduce data and address size from 8 to 4 bits
#TODO Reduce burst length
#TODO Reduce long/short space ratio
#TODO Make burst time based on tx frequency, so that higher frequencies reduce tx time
#TODO Reduce Start block size 
#TODO Evaluate possibility of a second, delayed transmission. This is to give a 2nd chance at capturing a corrupted transmission

from ir_tx import IR, STOP

_TBURST = 563
_T_ONE = 1687

class SLAM(IR):
    valid = (0xf, 0xf, 0)  # Max addr, data, toggle

    #DONE change asize argument passed to super().__init__() to new size
    # asize = on/off times (μs)
    # 2 on/off times per bit. 
    # NEC asize is 68 for 32 bits of data + start and end blocks
    # 8*4 + 2 = 34 bits

    # SLAM has 4 bit addr and data sizes. Additional 4 bits each of error detection, and Start and End bloc
    # 4*4 + 2 = 18 bits
    # SLAM asize = 36

    def __init__(self, pin, freq=38000, verbose=False):  # 38kHz is the standard frequency
        super().__init__(pin, freq, 36, 33, verbose)  # Measured duty ratio 33% 

    def _bit(self, b):
        self.append(_TBURST, _T_ONE if b else _TBURST) # If bit =1, long space, else short space

    #NOTE In nec.py, StartBlock times are 9ms on then 4.5ms off
    # However, the default wait times in ir_rx/nec.py are 4ms and 3ms

    def tx(self, addr, data, _):  # Ignore toggle
        self.append(4500, 2500) #Start Block TODO
        addr |= ((addr ^ 0xf) << 4)
        for _ in range(8):
            self._bit(addr & 1)
            addr >>= 1
        data |= ((data ^ 0xf) << 4)
        for _ in range(8):
            self._bit(data & 1)
            data >>= 1
        self.append(_TBURST)
