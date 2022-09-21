#******************************************************************************
#* @file    STM32U5_TrustZone_Disable.sh
#* @author  MCD Application Team
#* @brief   Disables TrustZone on STM32U5
#******************************************************************************
# * Copyright (c) 2021 STMicroelectronics.
#
#  * All rights reserved.
#
#  * This software is licensed under terms that can be found in the LICENSE file
#
#  * in the root directory of this software component.
#
#  * If no LICENSE file comes with this software, it is provided AS-IS.
#*****************************************************************************

read -p "Disabling trustzone requires that a trustzone enabled project is running on the board. Proceed (Y/[N])?" REPLY
if [[ $REPLY != [Yy]* ]]; then
    exit 1
fi


# Determine OS to find Cube Programmer Path
if [[ "$OSTYPE" == "darwin"* ]]; then
    ST_PROGRAMMER_PATH="/Applications/STMicroelectronics/STM32Cube/STM32CubeProgrammer/STM32CubeProgrammer.app/Contents/MacOs/bin/STM32_Programmer_CLI" 
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    ST_PROGRAMMER_PATH="/home/$USER/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI"
elif [[ "$OSTYPE" == "msys"* ]]; then
    ST_PROGRAMMER_PATH="C:/Program Files (x86)/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI.exe"
    if [[ ! -f "$ST_PROGRAMMER_PATH" ]]; then
        ST_PROGRAMMER_PATH="C:/Program Files/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI.exe"
    fi
else
    exit 1
fi


"$ST_PROGRAMMER_PATH" -c port=SWD mode=HotPlug -ob nSWBOOT0=0 nBOOT0=0
"$ST_PROGRAMMER_PATH" -c port=SWD mode=HotPlug -ob RDP=0xDC
"$ST_PROGRAMMER_PATH" -c port=SWD mode=HotPlug -ob RDP=0xAA TZEN=0
"$ST_PROGRAMMER_PATH" -c port=SWD mode=HotPlug -ob nSWBOOT0=1 nBOOT0=1