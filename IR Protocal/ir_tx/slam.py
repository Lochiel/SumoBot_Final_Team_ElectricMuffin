# SumoBot Little Asynchronous Messaging - SLAM 
# Encoder for IR transmission of SumoBots
# Written by Cam Chalmers
# For ECEN 2440 - Applications of Embedded Systems, Spring '24
# Modified NEC code
# Based on code by Peter Hinch

#TODO Reduce data and address size from 8 to 4 bits
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

    def __init__(self, pin, freq=38000, verbose=False):  # 38kHz is the standard frequency
        super().__init__(pin, freq, 68, 33, verbose)  # Measured duty ratio 33%

    def _bit(self, b):
        self.append(_TBURST, _T_ONE if b else _TBURST) # If bit =1, long space, else short space

    def tx(self, addr, data, _):  # Ignore toggle
        self.append(9000, 4500) #Start Block TODO
        for _ in range(0xf):
            self._bit(addr & 1)
            addr >>= 1
        data |= ((data ^ 0xf) << 4)
        for _ in range(0xf):
            self._bit(data & 1)
            data >>= 1
        self.append(_TBURST)

    # def repeat(self):
    #     self.aptr = 0
    #     self.append(9000, 2250, _TBURST)
    #     self.trigger()  # Initiate physical transmission.
