#!/usr/bin/python3

import time
import sys
import subprocess
import shutil

# Choose and program "display code"

while True:
	print ('Choose the display code related at the screen you are mounting.')
	print ('01: TIANMA TM104SDHG30 10" 800X600 RGB24 parallel display')
	
	display_code = input('Insert display code: ')
	if (display_code != '01'):
		print ('Display code no recognized. Please insert a display code in the list above.')
		continue
	break

# Write display code to eeprom (2 bytes)
f_eeprom = open('/sys/bus/i2c/drivers/at24/2-0050/eeprom','rb+')
f_eeprom.seek(199)
f_eeprom.write(display_code.encode('utf-8'))

# Read DT code programmed
f_eeprom.seek(195)
dt_code = f_eeprom.read(6).decode('utf-8')
dt_code = dt_code + '.dtb'
f_eeprom.close()
	
# Copy and rename device tree to be loaded during the boot
if subprocess.run(['mount', '-o', 'remount,rw', '/'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
	shutil.copyfile('/' + dt_code,'/vdwcontroller.dtb')
else:
	print('Error to mount in RW rootfs.')
	sys.exit(1)
subprocess.run(['mount', '-o', 'remount,ro', '/'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print('The system will be rebooted now...')
time.sleep(3)
subprocess.run(['reboot'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
