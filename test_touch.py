#!/usr/bin/python3

import os
import subprocess
import argparse
from common import *

###############################################################################
#	class Test_touch
###############################################################################
class Test_touch(Test_basic):
	def __init__(self):
		Test_basic.__init__(self, 'touch')
		self.err_dict['CALIBRATE_NOT_FOUND'] = 'Calibration script not found'
		self.err_dict['CALIBRATE_FAILED'] = 'Calibrate failed'

	def initialize(self):
		Test_basic.initialize(self)

	def finalize(self):
		try:
			Test_basic.finalize(self)
		except Test_error as e:
			sys.exit(-1)

	def calibrate(self):
		cal = '/home/vdw/customer_privileged_scripts/calibrate.sh'
		if not os.path.exists(cal):
			raise Test_error(self, 'CALIBRATE_NOT_FOUND')
		if subprocess.run([cal]).returncode != 0:
			raise Test_error(self, 'CALIBRATE_FAILED')

###############################################################################
try:
	t = Test_touch()
	
	parser = argparse.ArgumentParser(description='Test touch')
	t.add_common_arguments(parser)
	args = parser.parse_args()
	t.copy_common_arguments(args)

	t.initialize()

	t.message('Calibrate touchscreen...')
	t.calibrate()

	t.success()

except Test_error as e:
	e.test.error(e.code, e.value)
