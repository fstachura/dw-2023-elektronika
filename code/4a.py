# OLED 1.3 I2C

import machine
from lcd import SH1106_I2C

i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))
disp = SH1106_I2C(128, 64, i2c, addr=0x3c) #0x3c/0xbc
disp.fill(0)
disp.rotate(True)
disp.text('Testing 1', 0, 0, 1)
disp.show()

