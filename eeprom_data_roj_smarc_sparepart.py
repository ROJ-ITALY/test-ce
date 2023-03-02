#!/usr/bin/python3

import shutil
import sys
import subprocess
import datetime

# Data to program in ROJ: spare part SMARC_SN, empty CB_SN, DATE, display_code already '01'

# Read SMARC_SN
smarc_sn = input('Insert SMARC SN: ')
smarc_code = smarc_sn[:3]
smarc_code4 = smarc_sn[:4]
if (smarc_code == '909'):
    smarc_code = '01'
elif (smarc_code == '939' or smarc_code4 == '1049'):
    smarc_code = '02'
else:
    print ('smarc_code no recognized.')
    sys.exit(1)

# Don't read CB_SN
cb_sn = '0'
cb_code = '01'

# Read DATE
dt = datetime.datetime.utcnow()
dt_str = '{:0>4d}{:0>2d}{:0>2d}{:0>2d}{:0>2d}{:0>2d}'.format(dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second)

# Write buffer (63 bytes) to eeprom 
buffer = 'SMARC ' + smarc_sn + '\n' + 'CB ' + cb_sn + '\n' + 'DATE ' + dt_str + '\n'
f_eeprom = open('/sys/bus/i2c/drivers/at24/2-0050/eeprom','w')
f_eeprom.seek(0)
f_eeprom.write(buffer)

# DT CODE
display_code = '01'
dt_code = 'DT ' + smarc_code + cb_code + display_code + '\n'
# Write dt_code to eeprom (10 bytes)
f_eeprom.seek(192)
f_eeprom.write(dt_code)
f_eeprom.close()

dt_code = smarc_code + cb_code + display_code + '.dtb'

# Copy and rename device tree to be loaded during the boot
if subprocess.run(['mount', '-o', 'remount,rw', '/mnt/ro'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
	shutil.copyfile('/mnt/ro/' + dt_code,'/mnt/ro/vdwcontroller.dtb')
else:
	print('Error to mount in RW rootfs.')
	sys.exit(3)
	
subprocess.run(['mount', '-o', 'remount,ro', '/mnt/ro'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print ('eeprom programmed correctly!')
sys.exit(0)
