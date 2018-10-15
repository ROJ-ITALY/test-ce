#!/usr/bin/python3

import os
import subprocess
import time
import argparse
from common import *

###############################################################################
#	class Test_touch
###############################################################################
class Test_touch(Test_basic):
	def __init__(self):
		Test_basic.__init__(self, 'touch')
		f_eeprom = open('/sys/bus/i2c/drivers/at24/2-0050/eeprom','rb')
		f_eeprom.seek(199)
		self.dt = f_eeprom.read(2).decode('utf-8')
		self.err_dict['NO_DEVICE_INFO'] = 'Configuration not correct in eeprom or config file'
		self.err_dict['NO_TOUCH'] = 'AR1100 HID-MOUSE not detected'
		
	def initialize(self):
		Test_basic.initialize(self)

	def finalize(self):
		try:
			Test_basic.finalize(self)
		except Test_error as e:
			sys.exit(-1)

	def check_touch(self):
		if (not self.dt in self.config["displays"]):
			raise Test_error(self,'NO_DEVICE_INFO')
		dev = self.config["displays"][self.dt]["device"]
		t.message('Check touch {}'.format(dev))
		if (not subprocess.run(['sh', '-c', 'dmesg | grep {}'.format(dev)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0):
			raise Test_error(self,'NO_TOUCH')

###############################################################################
try:
	t = Test_touch()

	parser = argparse.ArgumentParser(description='Test touch')
	t.add_common_arguments(parser)
	args = parser.parse_args()
	t.copy_common_arguments(args)

	t.initialize()

	t.check_touch()

	t.success()

except Test_error as e:
	e.test.error(e.code, e.value)
