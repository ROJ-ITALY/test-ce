#!/usr/bin/python3

import os
import subprocess
import datetime

# Final Assembly data to program in China: PN_CE, SN_CE, DATE

# Read PN_CE
pn_ce = input('Insert PN Ce: ')

# Read SN_CE
sn_ce = input('Insert SN Ce: ')

# Read DATE
dt = datetime.datetime.utcnow()
dt_str = '{:0>4d}{:0>2d}{:0>2d}{:0>2d}{:0>2d}{:0>2d}'.format(dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second)

# Write buffer to eeprom (47 bytes)
buffer = 'PN ' + pn_ce + '\n' + 'SN ' + sn_ce + '\n' + 'DATE ' + dt_str + '\n'
f_eeprom = open('/sys/bus/i2c/drivers/at24/2-0050/eeprom','r+')
f_eeprom.seek(128)
f_eeprom.write(buffer)
f_eeprom.close()

# Remove device tree except vdwcontroller.dtb
if subprocess.run(['mount', '-o', 'remount,rw', '/'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
	path = '/'
	device_tree = [f for f in os.listdir(path) if f.endswith('.dtb')]
	for dt in device_tree:
		if (dt != 'vdwcontroller.dtb'):
			os.remove(path + dt)
	subprocess.run(['mount', '-o', 'remount,ro', '/'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print ('eeprom programmed correctly!')