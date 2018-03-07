#!/usr/bin/python3

import os
import subprocess
import time
import argparse
from common import *

###############################################################################
#	class Test_lan
###############################################################################
class Test_lan(Test_basic):
	def __init__(self):
		Test_basic.__init__(self, 'lan')
		self.err_dict['IF_NOT_FOUND'] = 'Interface \'%s\' not found'
		self.err_dict['PING_FAILED'] = 'Ping failed'

	def initialize(self):
		Test_basic.initialize(self)
		self.if_name = 'enp0s3'

	def finalize(self):
		try:
			Test_basic.finalize(self)
		except Test_error as e:
			sys.exit(-1)

	def check_interface(self):
		return subprocess.run(['ip', 'address', 'show', self.if_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0

	def get_mac_address(self):
		ret = subprocess.run(['ip', 'address', 'show', self.if_name], stdout=subprocess.PIPE)
		mac_address = self.simple_re(ret.stdout.decode('utf-8'), '.*link/ether ([0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2})')
		return mac_address

	def get_ip_address(self):
		ret = subprocess.run(['ip', 'address', 'show', self.if_name], stdout=subprocess.PIPE)
		ip_address = self.simple_re(ret.stdout.decode('utf-8'), '.*inet ([0-9]*\.[0-9]*\.[0-9]*\.[0-9]*)')
		return ip_address

	def ping(self):
		if subprocess.run(['ping', self.target, '-q', '-c', '3'], stdout=subprocess.DEVNULL).returncode != 0:
			raise Test_error(self, 'PING_FAILED')

###############################################################################
try:
	t = Test_lan()

	parser = argparse.ArgumentParser(description='Test LAN')
	t.add_common_arguments(parser)
	parser.add_argument('-t', '--target', type=str, default=t.config['lan']['target'], help="set target IP address to ping")
	args = parser.parse_args()
	t.copy_common_arguments(args)
	t.target = args.target

	t.initialize()

	t.message('Check interface')
	if not t.check_interface():
		raise Test_error(t, 'IF_NOT_FOUND', t.if_name)

	t.message('Get IP address')
	ip_address = t.get_ip_address()
	t.message('IP address: %s' % ip_address)

	t.message('Get MAC address')
	ip_address = t.get_mac_address()
	t.info('MAC address', ip_address)

	t.message('Ping %s' % t.target)
	t.ping()

	t.success()

except Test_error as e:
	e.test.error(e.code, e.value)
