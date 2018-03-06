#!/usr/bin/python3

import os
import sys
import subprocess
import argparse

###############################################################################
#	Scheduler_error
###############################################################################
class Scheduler_error(Exception):
	def __init__(self, msg):
		self.msg = msg
		
###############################################################################
def start(i, n, name):
	print('--------------------')
	print(' %s/%s  %s' % (i, n, name))
	print('--------------------')
	if name == 'calibrate':
		ret = subprocess.call(['/home/vdw/customer_privileged_scripts/calibrate.sh'])
	return ret;

test_list = ['calibrate']
arg_test_list = list(test_list)
arg_test_list.append('all')

parser = argparse.ArgumentParser(description='Test scheduler')
parser.add_argument('-c', '--count', type=int, default=1, help="set number of iterations")
parser.add_argument('--nostop', action="store_true", help="continue on error")
parser.add_argument('tests', type=str, choices=arg_test_list, nargs='*', help='tests list')
args = parser.parse_args()

if os.getuid() != 0:
	print('Error: non root')
	sys.exit(-1)

if args.tests == None:
	tests = test_list
else:
	tests = args.tests

error_found = False
try:
	n = args.count
	for i in range(0, n):
		for t in tests:
			if t == 'all':
				for t1 in test_list:
					if start(i+1, n, t1) != 0:
						error_found = True
						if not args.nostop:
							raise Scheduler_error(t1)
			else:
				if start(i+1, n, t) != 0:
					error_found = True
					if not args.nostop:
						raise Scheduler_error(t)

except Scheduler_error as e:
	sys.exit(-1)

sys.exit(0)
