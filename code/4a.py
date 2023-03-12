# Library taken from https://github.com/raspberrypi/pico-micropython-examples/blob/master/i2c/1106oled/sh1106.py
# MicroPython SH1106 OLED driver, I2C and SPI interfaces
# Copyright (c) 2016 Radomir Dopieralski (@deshipu),
#               2017 Robert Hammelrath (@robert-hh)
# Check LICENSE for licensing details

# OLED 1.3 I2C

from micropython import const
import utime as time
import framebuf


# a few register definitions
_SET_CONTRAST        = const(0x81)
_SET_NORM_INV        = const(0xa6)
_SET_DISP            = const(0xae)
_SET_SCAN_DIR        = const(0xc0)
_SET_SEG_REMAP       = const(0xa0)
_LOW_COLUMN_ADDRESS  = const(0x00)
_HIGH_COLUMN_ADDRESS = const(0x10)
_SET_PAGE_ADDRESS    = const(0xB0)


class SH1106:
    def __init__(self, width, height, external_vcc):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        fb = framebuf.FrameBuffer(self.buffer, self.width, self.height,
                                  framebuf.MVLSB)
        self.framebuf = fb
# set shortcuts for the methods of framebuf
        self.fill = fb.fill
        self.fill_rect = fb.fill_rect
        self.hline = fb.hline
        self.vline = fb.vline
        self.line = fb.line
        self.rect = fb.rect
        self.pixel = fb.pixel
        self.scroll = fb.scroll
        self.text = fb.text
        self.blit = fb.blit

        self.init_display()

    def init_display(self):
        self.reset()
        self.fill(0)
        self.poweron()
        self.show()

    def poweroff(self):
        self.write_cmd(_SET_DISP | 0x00)

    def poweron(self):
        self.write_cmd(_SET_DISP | 0x01)

    def rotate(self, flag, update=True):
        if flag:
            self.write_cmd(_SET_SEG_REMAP | 0x01)  # mirror display vertically
            self.write_cmd(_SET_SCAN_DIR | 0x08)  # mirror display hor.
        else:
            self.write_cmd(_SET_SEG_REMAP | 0x00)
            self.write_cmd(_SET_SCAN_DIR | 0x00)
        if update:
            self.show()

    def sleep(self, value):
        self.write_cmd(_SET_DISP | (not value))

    def contrast(self, contrast):
        self.write_cmd(_SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(_SET_NORM_INV | (invert & 1))

    def show(self):
        for page in range(self.height // 8):
            self.write_cmd(_SET_PAGE_ADDRESS | page)
            self.write_cmd(_LOW_COLUMN_ADDRESS | 2)
            self.write_cmd(_HIGH_COLUMN_ADDRESS | 0)
            self.write_data(self.buffer[
                self.width * page:self.width * page + self.width
            ])

    def reset(self, res):
        if res is not None:
            res(1)
            time.sleep_ms(1)
            res(0)
            time.sleep_ms(20)
            res(1)
            time.sleep_ms(20)


class SH1106_I2C(SH1106):
    def __init__(self, width, height, i2c, res=None, addr=0x3c,
                 external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        self.res = res
        self.temp = bytearray(2)
        if res is not None:
            res.init(res.OUT, value=1)
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.temp[0] = 0x80  # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_data(self, buf):
        self.i2c.writeto(self.addr, b'\x40'+buf)

    def reset(self):
        super().reset(self.res)


import machine

i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))
disp = SH1106_I2C(128, 64, i2c, addr=0x3c) #0x3c/0xbc
disp.fill(0)
disp.rotate(True)
disp.text('Testing 1', 0, 0, 1)
disp.show()
