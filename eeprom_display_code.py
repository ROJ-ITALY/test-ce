#!/usr/bin/python3

import time
import sys
import subprocess
import shutil
import json

# Choose and program "display code"

with open('config.json') as f:
	config = json.load(f)

displays = config["displays"]

while True:
	print ('Choose the display code related to the screen you are mounting:\n')
	for k,val in displays.items():
		print ('{}: {}'.format(k,val["info"]))
	print ('')
	display_code = input('Insert display code: ')
	if ( not display_code in displays ):
		print ('\n\033[31mDisplay code no recognized. Please choose a valid code from the list.\033[0m')
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
if subprocess.run(['/home/prod/scripts/update_bsp.sh'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
	print('Finished updating bsp.')
else:
	print('Error updating bsp.')
	sys.exit(1)

print('The system will be rebooted now...')
subprocess.run(['reboot'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

