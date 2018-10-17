#!/usr/bin/python3

import os
import subprocess
import time
import argparse
from common import *

###############################################################################
#	class Test_usb
###############################################################################
class Test_usb(Test_basic):
	def __init__(self):
		Test_basic.__init__(self, 'usb')
		self.err_dict['LABEL_A_FAILED'] = 'Check pen drive A failed or label A not found'
		self.err_dict['CHECK_A_FAILED'] = 'Check pen drive A failed or invalid pen drive A'
		self.err_dict['MOUNT_A_FAILED'] = 'Mount pen drive A failed'
	
	def initialize(self):
		Test_basic.initialize(self)

	def finalize(self):
		try:
			Test_basic.finalize(self)
		except Test_error as e:
			sys.exit(-1)

	def check(self):
		self.message('Check USB key A')
		mnt_path = '/mnt/{}'.format(self.label_a)
		dev = '/dev/disk/by-label/{}'.format(self.label_a)
		if not os.path.isdir(mnt_path):
			os.mkdir(mnt_path)
		if not os.path.exists(dev):
			raise Test_error(self, 'LABEL_A_FAILED')
		if subprocess.run(['mount', dev, mnt_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0:
			subprocess.run(['umount', mnt_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
			raise Test_error(self, 'MOUNT_A_FAILED')
		if subprocess.run(['sha256sum', '-c', 'test-file.sha256'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=mnt_path).returncode != 0:
			subprocess.run(['umount', mnt_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
			raise Test_error(self, 'CHECK_A_FAILED')
		subprocess.run(['umount', mnt_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

###############################################################################
try:
	t = Test_usb()
	
	parser = argparse.ArgumentParser(description='Test USB')
	t.add_common_arguments(parser)
	parser.add_argument('--labela', type=str, default=t.config['usb']['labela'], help="set pen drive A label")
	args = parser.parse_args()
	t.copy_common_arguments(args)
	t.label_a = args.labela

	t.initialize()

	t.check()

	t.success()

except Test_error as e:
	e.test.error(e.code, e.value)


