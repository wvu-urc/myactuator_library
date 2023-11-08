# MyActuatorMotor.py
# By: Nathan Adkins 
# email: npa00003@mix.wvu.edu
# WVU URC 

'''
https://www.robotshop.com/products/myactuator-rmd-x10-s2-v3-bldc-can-bus-reduction-ratio-135-w-new-driver-mc-x-500o

1.1.CAN Bus
    1.1.1. Parameters
        Bus interface: CAN
        Baud rate: 1Mbps
    1.1.2. Message format
        Identifier: Single motor command sending: 0x140 + ID(1~32)
            Multi-motor command sending: 0x280
            Reply: 0x240 + ID (1~32)
        Frame format: data frame
        Frame Type: Standard Frame
        DLC: 8 bytes
1.2.RS485 bus
    1.2.1. Parameters
        Bus interface: RS485
        Baudrate:115200bp,500Kbps,1Mbps,1.5Mbps,2Mbps

'''

import numpy as np
import can
from _MyActuatorMotorPrivate import _MyActuatorMotorPrivate

class MyActuatorMotor(_MyActuatorMotorPrivate):


    def __init__(self, arbitration_id):
        super().__init__(arbitration_id)


    # --------------------------------------------------------------------------------------------------------
    # THIS IS STAYING HERE FOR NOW WHILE THE LIBRARY GETS OVERHAULED FOR V2. DO NOT REMOVE. THX FUTURE NATE <3
    def make_rpm_command(self, rpm):

            rpm_integer = np.int32(rpm / .01)

            can_data = [0xA2, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
            can_data[4:7] = self.int32_to_uint8(rpm_integer)

            return can.Message(
                arbitration_id = self.arbitration_id,
                is_extended_id = self.is_extended_id,
                data = can_data
                )
    # THIS IS STAYING HERE FOR NOW WHILE THE LIBRARY GETS OVERHAULED FOR V2. DO NOT REMOVE. THX FUTURE NATE <3
    # --------------------------------------------------------------------------------------------------------


    def make_rpm_command_new(self, rpm):

        def rpm_to_dps(rpm_val):
            return rpm_val * 6 
        
        dps = rpm_to_dps(rpm)

        dps = np.int32(dps / .01)

        can_data = [0xA2, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        can_data[4:7] = self.int32_to_uint8(dps)
    

    def int32_to_uint8(self,byte_32):
        byte_3 = (byte_32 >> 24)
        byte_2 = (byte_32 >> 16) & 0xFF
        byte_1 =  (byte_32 >> 8) & 0xFF
        byte_0 = byte_32 & 0xFF
        bytes = np.array([byte_0, byte_1, byte_2, byte_3], dtype=np.uint8)
        return bytes
    