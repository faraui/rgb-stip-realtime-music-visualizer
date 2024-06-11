import serial

class RGBStrip:
    def __init__(self, port='/dev/ttyUSB0'): # LED srip TTY/COM device absolute path
        self.strip = serial.Serial(port, 2000000)

    def setColor(self, color): # color in integer format (0xRRGGBB)
        self.strip.write(color.to_bytes(3, 'big'))

    def setColorRgb(self, r, g, b):
        self.setColor(r<<16 | g<<8 | b)
