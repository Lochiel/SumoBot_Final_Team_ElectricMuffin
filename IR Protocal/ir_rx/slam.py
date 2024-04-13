# Decoder for IR transmission of SumoBots
# Written by Cam Chalmers
# For ECEN 2440 - Applications of Embedded Systems, Spring '24
# Modified NEC code
# Based on code by Peter Hinch

#DONE Remove non-SLAM handling; Samsung, NEC-8 etc.
#DONE Reduce data and address size from 8 to 4 bits
#TODO Reduce burst length
#TODO Make burst time based on tx frequency, so that higher frequencies reduce tx time
#TODO Reduce Start block size 
# Changed first burst from 9ms to 2.5 ms. 2.5 ms is supported by the Samsung standard, so it's presumed to have been tested
# We should still test and find a shorter burst
#TODO Evaluate possibility of a second, delayed transmission. This is to give a 2nd chance at capturing a corrupted transmission

from utime import ticks_us, ticks_diff
from ir_rx import IR_RX

class SLAM(IR_RX):
    
    #NOTE In nec.py, StartBlock times are 9ms on then 4.5ms off
    # However, the default wait times in ir_rx/nec.py are 4ms and 3ms
    def __init__(self, pin, callback, *args):
        self._edges = 36 #Number of expected edges
        self._txBlock = 45 #Number of ms to wait for a full tx. 
        # Block lasts <= 45ms and has 36 edges
        super().__init__(pin, self._edges, self._txBlock, callback, *args)
        self._addr = 0
        self.StarBlock_leader = 4000 # Length of Start Block
        self.StarBlock_follower = 2000


    def decode(self, _):
        try:
            if self.edge > self._edges:
                raise RuntimeError(self.OVERRUN)
            width = ticks_diff(self._times[1], self._times[0])
            if width < self.StarBlock_leader:  # 2.5ms leading mark for all valid data
                raise RuntimeError(self.BADSTART)
            width = ticks_diff(self._times[2], self._times[1])
            if width > self.StarBlock_follower:  # 4.5ms space for normal data
                if self.edge < self._edges:  # Haven't received the correct number of edges
                    raise RuntimeError(self.BADBLOCK)
                # Time spaces only (marks are always 562.5µs)
                # Space is 1.6875ms (1) or 562.5µs (0)
                # Skip last bit which is always 1
                val = 0
                for edge in range(3, self._edges - 2, 2):
                    val >>= 1
                    if ticks_diff(self._times[edge + 1], self._times[edge]) > 1120:
                        val |= 0x8000  #make val the size of data transmission; each '0' is 4 bits
            else:
                raise RuntimeError(self.BADSTART)
            
            addr = val & 0xf  # 4 bit addr
            if addr != ((val >> 4) ^ 0xf) & 0xf:  # 4 bit addr doesn't match check
                raise RuntimeError(self.BADADDR)
            self._addr = addr

            cmd = (val >> 8) & 0xf
            if cmd != (val >> 12) ^ 0xf:
                raise RuntimeError(self.BADDATA)

        except RuntimeError as e:
            cmd = e.args[0]
            addr =  0
        # Set up for new data burst and run user callback
        self.do_callback(cmd, addr, 0)