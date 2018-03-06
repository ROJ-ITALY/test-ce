#!/usr/bin/python3

import os
import argparse
from common import *

###############################################################################
#    class Test_display
###############################################################################
class Test_display(Test_basic):

    def __init__(self):
         Test_basic.__init__(self, 'display')
         self.io_dict = {
            'gpio5': 71,
            'gpio6': 72,
            'avdd_set': 171,
            'vgh_set': 170,
            'incesh_bl': 167,
            'vcom_set': 39
        }
        self.err_dict['WRONG_DISPLAY'] = 'Display %s inches not recognized'

    def gpio_export(self,name):
        i = self.io_dict[name]
        if not os.path.exists('/sys/class/gpio/gpio%d' % i):
            write_int_to_file('/sys/class/gpio/export', i)

    def gpio_export_all(self):
        for io in self.io_dict:
            self.gpio_export(io)

    def gpio_unexport(self,name):
        i = self.io_dict[name]
        if os.path.exists('/sys/class/gpio/gpio%d' % i):
            write_int_to_file('/sys/class/gpio/unexport', i)

    def gpio_unexport_all(self):
        for io in self.io_dict:
            self.gpio_unexport(io)

    def gpio_direction(self,name,d):
        i = self.io_dict[name]
        write_str_to_file('/sys/class/gpio/gpio%d/direction' % i, d)

    def gpio_write(self,name, v):
        i = self.io_dict[name]
        write_int_to_file('/sys/class/gpio/gpio%d/value' % i, v)

    def gpio_read(self,name):
        i = self.io_dict[name]
        return read_int_from_file('/sys/class/gpio/gpio%d/value' % i);

    def init(self):
        self.gpio_export_all()
        self.gpio_direction('gpio5','in')
        self.gpio_direction('gpio6','in')
        self.gpio_direction('avdd_set','out')
        self.gpio_direction('vgh_set','out')
        self.gpio_direction('incesh_bl','out')
        self.gpio_direction('vcom_set','out')

    def deinit(self):
        self.gpio_unexport_all()




###############################################################################
#    main
###############################################################################

try:

    t = Test_display()

    if os.getuid() != 0:
        raise Test_error(t, 'NON_ROOT')

    parser = argparse.ArgumentParser(description='Test DISPLAY')
    t.add_common_arguments(parser)
    parser.add_argument('-d', '--display', type=int, choices=[7, 10], default=t.config['display']['display'], help="set display size [inches]")
    args = parser.parse_args()
    t.copy_common_arguments(args)

    t.display = args.display

    t.init()
    gp5 = t.gpio_read('gpio5')
    gp6 = t.gpio_read('gpio6')

    if t.display == 7:
        t.message("Check display 7 inches.")
        if gp5 == 0 and gp6 ==1:
            t.message("Recognized display 7 inches.")
            t.message("Set voltage and current for display 7 inches.")
            t.gpio_write('avdd_set', 0)
            t.gpio_write('vgh_set', 0)
            t.gpio_write('incesh_bl', 0)
            t.gpio_write('vcom_set', 0)
        else:
            t.deinit()
            raise Test_error(t, 'WRONG_DISPLAY', t.display)
    else:
        t.message("Check display 10 inches.")
        if gp5 == 1 and gp6 ==1:
            t.message("Recognized display 10 inches.")
            t.message("Set voltage and current for display 10 inches.")
            t.gpio_write('avdd_set', 1)
            t.gpio_write('vgh_set', 1)
            t.gpio_write('incesh_bl', 1)
            t.gpio_write('vcom_set', 0)
        else:
            t.deinit()
            raise Test_error(t, 'WRONG_DISPLAY', t.display)

    t.deinit()
    t.success()

except Test_error as e:
    e.test.error(e.code, e.value)
