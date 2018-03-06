#!/usr/bin/python3

import os
import sys
import json

###############################################################################
#	write_str_to_file
###############################################################################
def write_str_to_file(filename, value):
	f = open(filename, 'w')
	f.write(value)
	f.close

###############################################################################
#	write_int_to_file
###############################################################################
def write_int_to_file(filename, value):
	f = open(filename, 'w')
	f.write(str(value))
	f.close

###############################################################################
#	read_str_from_file
###############################################################################
def read_str_from_file(filename):
	f = open(filename, 'r')
	ret = f.readline()
	while len(ret) > 0 and (ret[-1] == '\r' or ret[-1] == '\n'):
		ret = ret[:-1]
	f.close
	return ret;

###############################################################################
#	read_int_from_file
###############################################################################
def read_int_from_file(filename):
	f = open(filename, 'r')
	ret = int(f.readline())
	f.close
	return ret;

###############################################################################
#	class Test_error
###############################################################################
class Test_error(Exception):
	def __init__(self, test, code, value=None):
		self.test = test
		self.code = code
		self.value = value

###############################################################################
#	class Test_basic
###############################################################################
class Test_basic:

	def __init__(self, name):
		self.err_dict = {
			'NON_ROOT': 'Non root'
		}
		self.COLOR_SUCCESS = '\033[92m'
		self.COLOR_INFO = '\033[93m'
		self.COLOR_ERROR = '\033[91m'
		self.COLOR_DEBUG = '\033[94m'
		self.COLOR_MESSAGE = '\033[94m'
		self.COLOR_DEFAULT = '\033[39m'
		self.name = name
		self.verbosity = 2
		self.color = True
		self.load_config()

	def success(self):
		s = '{}-OK'.format(self.name)
		if self.color:
			print(self.COLOR_SUCCESS + s + self.COLOR_DEFAULT)
		else:
			print(s)
		sys.exit(0)

	def error(self, code, value):
		if code in self.err_dict:
			err_txt = self.err_dict[code]
			if err_txt.find('%s') == -1:
				err_msg = err_txt
			else:
				err_msg = err_txt % (value)
		else:
			err_msg = 'Unknown error'
		s = '{}-ERR {} ({})'.format(self.name, code, err_msg)
		if self.color:
			print(self.COLOR_ERROR + s + self.COLOR_DEFAULT)
		else:
			print(s)
		sys.exit(-1)

	def info(self, name, value):
		s = '{}-INF {}={}'.format(self.name, name, value)
		if self.color:
			print(self.COLOR_INFO + s + self.COLOR_DEFAULT)
		else:
			print(s)

	def message(self, msg):
		s = '{}-MSG {}'.format(self.name, msg)
		if self.verbosity > 0:
			if self.color:
				print(self.COLOR_MESSAGE + s + self.COLOR_DEFAULT)
			else:
				print(s)

	def debug(self, msg):
		s = '{}-DBG {}'.format(self.name, msg)
		if self.verbosity > 1:
			if self.color:
				print(self.COLOR_DEBUG + s + self.COLOR_DEFAULT)
			else:
				print(s)

	def set_verbosity(self, level):
		self.verbosity = level

	def add_common_arguments(self, parser):
		parser.add_argument('-v', '--verbosity', type=int, choices=[0,1,2], default=self.config['verbosity'], help="set verbosity")
		parser.add_argument('--color', type=str, choices=['yes', 'no'], default=self.config['colorize'], help="colorize the output")

	def copy_common_arguments(self, args):
		self.verbosity = args.verbosity
		self.color = (args.color == 'yes')

	def load_config(self):
		with open('config.json') as f:
			self.config = json.load(f)

