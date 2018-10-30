#!/usr/bin/python3

import os
import argparse
from common import *

###############################################################################
#	class Test_gpio
###############################################################################
class Test_gpio(Test_basic):
	def __init__(self):
		Test_basic.__init__(self, 'gpio')
		self.err_dict['CHECK_GPIO_USER_01_ERROR'] = 'USER_GPIO_0 USER_GPIO_1 error'
		self.err_dict['CHECK_GPIO_USER_23_ERROR'] = 'USER_GPIO_2 USER_GPIO_3 error'
		self.err_dict['CHECK_GPIO_USER_45_ERROR'] = 'USER_GPIO_4 USER_GPIO_5 error'
		self.err_dict['CHECK_GPIO_USER_67_ERROR'] = 'USER_GPIO_6 USER_GPIO_7 error'

	def initialize(self):
		Test_basic.initialize(self)

	def finalize(self):
		try:
			Test_basic.finalize(self)			
		except Test_error as e:
			sys.exit(-1)

	def check_user_gpio_01(self):
		Gpio.export('USER_GPIO_0')
		Gpio.export('USER_GPIO_1')
		Gpio.set_direction('USER_GPIO_0', 'out')
		Gpio.set_direction('USER_GPIO_1', 'in')
		Gpio.write('USER_GPIO_0',0)
		time.sleep(.1)
		ret = Gpio.read('USER_GPIO_1')
		Gpio.unexport('USER_GPIO_0')
		Gpio.unexport('USER_GPIO_1')
		return ret
		
	def check_user_gpio_23(self):
		Gpio.export('USER_GPIO_2')
		Gpio.export('USER_GPIO_3')
		Gpio.set_direction('USER_GPIO_2', 'out')
		Gpio.set_direction('USER_GPIO_3', 'in')
		Gpio.write('USER_GPIO_2',0)
		time.sleep(.1)
		ret = Gpio.read('USER_GPIO_3')
		Gpio.unexport('USER_GPIO_2')
		Gpio.unexport('USER_GPIO_3')
		return ret
		
	def check_user_gpio_45(self):
		Gpio.export('USER_GPIO_4')
		Gpio.export('USER_GPIO_5')
		Gpio.set_direction('USER_GPIO_4', 'out')
		Gpio.set_direction('USER_GPIO_5', 'in')
		Gpio.write('USER_GPIO_4',0)
		time.sleep(.1)
		ret = Gpio.read('USER_GPIO_5')
		Gpio.unexport('USER_GPIO_4')
		Gpio.unexport('USER_GPIO_5')
		return ret

	def check_user_gpio_67(self):
		Gpio.export('USER_GPIO_6')
		Gpio.export('USER_GPIO_7')
		Gpio.set_direction('USER_GPIO_6', 'out')
		Gpio.set_direction('USER_GPIO_7', 'in')
		Gpio.write('USER_GPIO_6',0)
		time.sleep(.1)
		ret = Gpio.read('USER_GPIO_7')
		Gpio.unexport('USER_GPIO_6')
		Gpio.unexport('USER_GPIO_7')
		return ret		

###############################################################################
try:
	t = Test_gpio()

	parser = argparse.ArgumentParser(description='Test gpio')
	t.add_common_arguments(parser)
	args = parser.parse_args()
	t.copy_common_arguments(args)

	t.initialize()

	t.message('Check USER_GPIO_0 - USER_GPIO_1')
	ret = t.check_user_gpio_01()
	if ret == 1:
		raise Test_error(t, "CHECK_GPIO_USER_01_ERROR")

	t.message('Check USER_GPIO_2 - USER_GPIO_3')
	ret = t.check_user_gpio_23()
	if ret == 1:
		raise Test_error(t, "CHECK_GPIO_USER_23_ERROR")

	t.message('Check USER_GPIO_4 - USER_GPIO_5')
	ret = t.check_user_gpio_45()
	if ret == 1:
		raise Test_error(t, "CHECK_GPIO_USER_45_ERROR")
		
	t.message('Check USER_GPIO_6 - USER_GPIO_7')
	ret = t.check_user_gpio_67()
	if ret == 1:
		raise Test_error(t, "CHECK_GPIO_USER_67_ERROR")	
	
	t.success()

except Test_error as e:
	e.test.error(e.code, e.value)

