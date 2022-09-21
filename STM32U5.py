#******************************************************************************
# * @file           : STM32U5.py
# * @brief          : Python Utility for STM32U5
# ******************************************************************************
# * @attention
# *
# * <h2><center>&copy; Copyright (c) 2022 STMicroelectronics.
# * All rights reserved.</center></h2>
# *
# * This software component is licensed by ST under BSD 3-Clause license,
# * the "License"; You may not use this file except in compliance with the
# * License. You may obtain a copy of the License at:
# *                        opensource.org/licenses/BSD-3-Clause
# ******************************************************************************

import serial
import serial.tools.list_ports
import platform
import string
import os
import time
from uuid import getnode as get_mac

BOARD_NAMES = ["DIS_U585AI", "NOD_U585AI"]
DEFAULT_BAUD = 115200
HWID = "VID:PID=0483:374"



class STM32U5:


    def __init__(self, baud=DEFAULT_BAUD):
        self.port = self.get_com()
        self.path = self.get_path()
        self.baud = baud
        self.name = self.get_name()

    

    # Get the board com port ####################################################################################################
    def get_com(self):
        ports = serial.tools.list_ports.comports()
        for p in ports:
            if HWID in p.hwid:
                return p.device
        
        raise Exception ( ' PORT ERR ' )




    # Get the board drive ####################################################################################################
    def get_path(self):
        USBPATH = ''
        op_sys = platform.system()
        if "windows" in op_sys.lower():
            # Find drive letter
            for l in string.ascii_uppercase:
                if os.path.exists('%s:\\MBED.HTM' % l):
                    USBPATH = '%s:\\' % l
                    break
            
        elif "linux" in op_sys.lower():
            user = os.getlogin()
            for board in BOARD_NAMES:
                temp_path = '/media/%s/%s/' % (user, board)
                if os.path.exists(temp_path):
                    USBPATH = temp_path
                    break
        elif ("darwin" in op_sys.lower()) or ('mac' in op_sys.lower()): # Mac
            for board in BOARD_NAMES:
                    temp_path = '/Volumes/%s/' % board
                    if os.path.exists(temp_path):
                        USBPATH = temp_path
                        break
        else:
            raise Exception ( ' OPERATING SYSTEM ERR ' )

        if USBPATH == '':
            raise Exception ( ' BOARD NOT FOUND ERR ' )
        
        return USBPATH



    # Indefinitely read serial communication ########################################################################################
    def serial_read(self):
        ser = serial.Serial(self.port, self.baud)

        #reading serial port indefinitely
        try:
            while True:
                if ser.in_waiting > 0:
                    print(ser.readline().decode("utf-8", errors='ignore'), end = '')
                    
                else: 
                    time.sleep(1)
        except KeyboardInterrupt:
            quit()

    



    # Write a msg to board over serial port ###########################################################################################
    def serial_write(self, msg):
        ser = serial.Serial(self.port, self.baud)
        ser.write(bytes(msg))
        ser.close()



    



    # Combines host mac address, device serial number, and com port number to return a semi unique device name ######################
    def get_name(self):
        ports = serial.tools.list_ports.comports()
        for p in ports:
            if HWID in p.hwid:
                mac = get_mac()
                device_id = 'stm32u5-' + hex(mac)[-5:-1] + p.serial_number[-5:] + p.device[-2:]
                return device_id
        
        raise Exception("Port Error")


    
    
    
    
    
    
    # Flash the board using drag and drop ###########################################################################################
    def flash_board(self, flashing_file, wait=False):

        session_os = platform.system()

        # In Windows
        if session_os == "Windows":
            cmd = 'copy "' + flashing_file + '" "' + self.path + 'File.bin"'
        else:
            cmd = 'cp "' + flashing_file + '" "' + self.path + 'File.bin"'

        err = os.system(cmd)
        if err!=0:
            raise Exception("Flashing Error")


        if wait:
            self.wait()







    # Wait for characters to come acroos the serial port #############################################################################
    def wait(self):
        port = serial.Serial(self.port, self.baud)

        bytesToRead = port.in_waiting
        while (port.in_waiting <= bytesToRead):
            time.sleep(0.1)

        port.close()
