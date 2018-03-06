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
		self.err_dict['CHECK1_FAILED'] = 'Check USB 1 failed or invalid USB key 1'
		self.err_dict['CHECK2_FAILED'] = 'Check USB 2 failed or invalid USB key 2'
		self.err_dict['MOUNT1_FAILED'] = 'Mount USB 1 failed'
		self.err_dict['MOUNT2_FAILED'] = 'Mount USB 2 failed'
	
	def initialize(self):
		Test_basic.initialize(self)

	def finalize(self):
		try:
			Test_basic.finalize(self)
		except Test_error as e:		
			sys.exit(-1)

	def check(self):
		ret = subprocess.run(['findmnt', '-S', 'LABEL=\"%s\"' % self.label1, '-n', '-o', 'TARGET'], stdout=subprocess.PIPE)
		path1 = ret.stdout.decode('utf-8')[:-1]
		if not os.path.exists(path1):
			raise Test_error(self, 'MOUNT1_FAILED')
		if subprocess.run(['sha256sum', '-c', 'test-file.sha256', '--quiet'], stdout=subprocess.DEVNULL, cwd=path1).returncode != 0:
			raise Test_error(self, 'CHECK1_FAILED')

		ret = subprocess.run(['findmnt', '-S', 'LABEL=\"%s\"' % self.label2, '-n', '-o', 'TARGET'], stdout=subprocess.PIPE)
		path2 = ret.stdout.decode('utf-8')[:-1]
		if not os.path.exists(path2):
			raise Test_error(self, 'MOUNT2_FAILED')
		if subprocess.run(['sha256sum', '-c', 'test-file.sha256', '--quiet'], stdout=subprocess.DEVNULL, cwd=path2).returncode != 0:
			raise Test_error(self, 'CHECK2_FAILED')

###############################################################################
try:
	t = Test_usb()
	
	parser = argparse.ArgumentParser(description='Test USB')
	t.add_common_arguments(parser)
	parser.add_argument('--label1', type=str, default=t.config['usb']['label1'], help="set pen drive 1 label")
	parser.add_argument('--label2', type=str, default=t.config['usb']['label2'], help="set pen drive 2 label")
	args = parser.parse_args()
	t.copy_common_arguments(args)
	t.label1 = args.label1
	t.label2 = args.label2

	t.initialize()

	t.check()

	t.success()

except Test_error as e:
	e.test.error(e.code, e.value)


