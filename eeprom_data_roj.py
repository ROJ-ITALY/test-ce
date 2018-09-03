#!/usr/bin/python3

import sys
import subprocess
import datetime

# Data to program in ROJ: SMARC_SN, CB_SN, DATE

# Read SMARC_SN
smarc_sn = input('Insert SMARC SN: ')
smarc_code = smarc_sn[:3]
if (smarc_code == '909'):
    smarc_code = '01'
elif (smarc_code == '939'):
    smarc_code = '02'
else:
    print ('smarc_code no recognized.')
    sys.exit(1)

# Read CB_SN
cb_sn = input('Insert CB SN: ')
cb_code = cb_sn[:3]
if (cb_code == '899'):
    cb_code = '01'
else:
    print ('cb_code no recognized.')
    sys.exit(2)

# Read DATE
dt = datetime.datetime.utcnow()
dt_str = '{:0>4d}{:0>2d}{:0>2d}{:0>2d}{:0>2d}{:0>2d}'.format(dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second)

# Write buffer (63 bytes) to eeprom 
buffer = 'SMARC ' + smarc_sn + '\n' + 'CB ' + cb_sn + '\n' + 'DATE ' + dt_str + '\n'
f_eeprom = open('/sys/bus/i2c/drivers/at24/2-0050/eeprom','w')
f_eeprom.seek(0)
f_eeprom.write(buffer)

# DT CODE
display_code = '00'
dt_code = 'DT ' + smarc_code + cb_code + display_code + '\n'
# Write dt_code to eeprom (10 bytes)
f_eeprom.seek(192)
f_eeprom.write(dt_code)
f_eeprom.close()

print ('eeprom programmed correctly!')
