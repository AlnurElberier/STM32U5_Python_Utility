::******************************************************************************
::* @file    STM32CubeProg_Reset.bat
::* @author  MCD Application Team
::* @brief   Issue a reset using ST-Link and STM32CubeProg.
::******************************************************************************
::* @attention
::*
::* <h2><center>&copy; COPYRIGHT 2015 STMicroelectronics</center></h2>
::*
::* Licensed under MCD-ST Liberty SW License Agreement V2, (the "License");
::* You may not use this file except in compliance with the License.
::* You may obtain a copy of the License at:
::*
::*        http://www.st.com/software_license_agreement_liberty_v2
::*
::* Unless required by applicable law or agreed to in writing, software 
::* distributed under the License is distributed on an "AS IS" BASIS, 
::* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
::* See the License for the specific language governing permissions and
::* limitations under the License.
::******************************************************************************

:: Use STM32Cube-Prog
if exist "C:\Program Files (x86)\STMicroelectronics\STM32Cube\STM32CubeProgrammer\bin\STM32_Programmer_CLI.exe" (
    set ST_LINK_PATH="C:\Program Files (x86)\STMicroelectronics\STM32Cube\STM32CubeProgrammer\bin\STM32_Programmer_CLI.exe" 
) else (
    set ST_LINK_PATH="C:\Program Files\STMicroelectronics\STM32Cube\STM32CubeProgrammer\bin\STM32_Programmer_CLI.exe"
)
echo on
%ST_LINK_PATH% -c port=swd -hardrst
::@echo off
