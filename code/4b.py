import machine
from lcd import SSD1306_SPI

spi = machine.SPI(0,
                  sck=machine.Pin(2, machine.Pin.OUT),
                  mosi=machine.Pin(3, machine.Pin.OUT),
                  miso=machine.Pin(0, machine.Pin.OUT))

disp = SSD1306_SPI(width=128, 
                   height=64, 
                   spi=spi, 
                   dc=machine.Pin(15, machine.Pin.OUT),
                   res=machine.Pin(14, machine.Pin.OUT),
                   cs=machine.Pin(1, machine.Pin.OUT))

disp.fill(0)
disp.text('Testing 1', 0, 0, 1)
disp.show()
