# 16x2 I2C

from machine import I2C, Pin
from lcd import I2cLcd

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
lcd.clear()
lcd.blink_cursor_on()
lcd.putstr("test")

