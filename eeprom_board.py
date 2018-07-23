#!/usr/bin/python3

import subprocess
import datetime

# Data to program in ROJ: SMARC_SN, CB_SN, DATE
# Read SMARC_SN
smarc_sn = input('Insert SMARC SN: ')
# Read CB_SN
cb_sn = input('Insert CB SN: ')
# Read DATE
dt = datetime.datetime.utcnow()
dt_str = '{:0>4d}{:0>2d}{:0>2d}{:0>2d}{:0>2d}{:0>2d}'.format(dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second)

buffer = 'SMARC ' + smarc_sn + '\n' + 'CB ' + cb_sn + '\n' + 'DATE ' + dt_str + '\n'
# Write buffer to eeprom (63 bytes)
f_eeprom = open('/sys/bus/i2c/drivers/at24/2-0050/eeprom','w')
f_eeprom.seek(1)
f_eeprom.write(buffer)
f_eeprom.close()

print ('eeprom programmed correctly!')