#!/usr/bin/python3

import os
import subprocess
import time
import argparse
from common import *

###############################################################################
#	class Test_sd
###############################################################################
class Test_sd(Test_basic):
	def __init__(self):
		Test_basic.__init__(self, 'sd')
		self.err_dict['CHECK_FAILED'] = 'Check SD'
		self.err_dict['MOUNT_FAILED'] = 'Mount SD failed'
	
	def initialize(self):
		Test_basic.initialize(self)

	def finalize(self):
		try:
			Test_basic.finalize(self)
		except Test_error as e:		
			sys.exit(-1)

	def check(self):
		mnt_path = '/mnt/sdcard'
		if subprocess.run(['findmnt', '-M', mnt_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0:
			raise Test_error(self, 'MOUNT_FAILED')
		p = mnt_path + os.sep + 'app_data'
		self.message('Check for \'%s\'' % p)
		if not os.path.isdir(p):
			raise Test_error(self, 'CHECK_FAILED')
		p = mnt_path + os.sep + 'users'
		self.message('Check for \'%s\'' % p)
		if not os.path.isdir(p):
			raise Test_error(self, 'CHECK_FAILED')

###############################################################################
try:
	t = Test_sd()
	
	parser = argparse.ArgumentParser(description='Test SD')
	t.add_common_arguments(parser)
	args = parser.parse_args()
	t.copy_common_arguments(args)

	t.initialize()

	t.check()

	t.success()

except Test_error as e:
	e.test.error(e.code, e.value)
