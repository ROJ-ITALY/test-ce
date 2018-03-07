#!/usr/bin/python3

import os
import argparse
from common import *

###############################################################################
#	class Test_fan
###############################################################################
class Test_fan(Test_basic):
	def __init__(self):
		Test_basic.__init__(self, 'fan')
		self.err_dict['FAN_FEEDBACK_ERROR'] = 'Fan feedback error'

	def initialize(self):
		Test_basic.initialize(self)

	def finalize(self):
		try:
			Test_basic.finalize(self)
			Gpio.unexport('IN_FAN_FB')
		except Test_error as e:
			sys.exit(-1)

	def get_fan_feedback(self):
		Gpio.export('IN_FAN_FB')
		ret = Gpio.read('IN_FAN_FB')
		Gpio.unexport('IN_FAN_FB')
		return ret

###############################################################################
try:
	t = Test_fan()

	parser = argparse.ArgumentParser(description='Test fan ')
	t.add_common_arguments(parser)
	args = parser.parse_args()
	t.copy_common_arguments(args)

	t.initialize()

	t.message('Get fan feedback')
	ret = t.get_fan_feedback()
	if ret == 0:
		Test_error(t, "FAN_FEEDBACK_ERROR")

	t.success()

except Test_error as e:
	e.test.error(e.code, e.value)


