import sys
import machine
import ssd1306
import time


def takeANap():
    """Hang a few milliseconds"""
    #machine.sleep(0.01)
    #machine.lightsleep(10)
    machine.idle()
    time.sleep_ms(10)


class ADC(machine.ADC):
    """superseed micropython's ADC class, hiding platform details.
    """

    if sys.platform == "esp32":
        #import esp32
        ADC_PIN = 32
        # esp32 ADC outputs an int up to 4096. It is reputated not reliable on its
        # first 10%, so we'll use an according FLOOR read value :
        OUTPUT_RANGE = 4096
        #self.adc.width(machine.ADC.WIDTH_9BIT)
    elif sys.platform == "esp8266":
        # esp8266 ADC outputs 1024 levels. Same remarks apply.
        OUTPUT_RANGE = 1024
    FLOOR = OUTPUT_RANGE / 10

    def __init__(self):
        if sys.platform == "esp32":
            super().__init__(machine.Pin(self.ADC_PIN))
            self.atten(machine.ADC.ATTN_11DB)
            self.width(machine.ADC.WIDTH_9BIT)
        elif sys.platform == "esp8266":
            super().__init__(0)

    def readMeaningfulValue(self):
        """Blocking call looping on the ADC until it reaches ADC.FLOOR
        (machine-specific sensible noise filter).
        """
        readValue = 0
        while int(readValue) < ADC.FLOOR:
            self.takeASmallNap()
            readValue = self.read()
        print(readValue)
        #return b"%04i" % readValue
        return readValue

    def takeASmallNap(self):
        """Hang 500 microseconds.
        """
        time.sleep(0.0005)


class Relay(machine.Pin):
    """Derive a relay switcher from machine.Pin .

    Note that you will have to select relevant RELAY_PIN .
    """

    #RELAY_PIN = 4              # D2 on the Wemos TTGO 0.91 OLED - used by the OLED
    RELAY_PIN = 15              # That's D8
    BLINK_LENGTH = 10           # In milliseconds

    def __init__(self):
        #super().__init__(self.RELAY_PIN, machine.Pin.OUT, value=0)
        super().__init__(self.RELAY_PIN, machine.Pin.OUT, 0)

    def blink(self):
        self.on()
        time.sleep_ms(self.BLINK_LENGTH)
        self.off()


def OLED():
    if sys.platform == "esp32":
        d = _OLEDDisplayEsp32()
    elif sys.platform == "esp8266":
        d = _OLEDDisplayEsp8266()
    return d


class _OLEDDisplay(ssd1306.SSD1306_I2C):
    """The real Oled display manager.

    This class must be superseeded by a class initializing :

        WIDTH
        HEIGHT
        CHAR_HEIGHT
        TXD1_PIN
        SDA_PIN
        CLK_PIN

    Note that self.pixel(x, y) would output value if we omit c=1 (on) or 0 (off).
    """

    WIDTH = 128
    HEIGHT = 32
    CHAR_SIZE = 8                            # OLED font char height
    SCREEN_LENGTH = int(WIDTH / CHAR_SIZE)   # OLED char per line
    SCREEN_HEIGHT = int(HEIGHT / CHAR_SIZE)  # OLED char per column

    def __init__(self):
        led_reset_pin = machine.Pin(self.SDA_PIN, machine.Pin.OUT)
        led_reset_pin.off()
        time.sleep(0.1)
        led_reset_pin.on()
        time.sleep(0.1)
        i2c = machine.I2C(
                scl=machine.Pin(self.CLK_PIN),
                sda=machine.Pin(self.TXD1_PIN),
                freq=100000
        )
        super().__init__(self.WIDTH, self.HEIGHT, i2c)

    def close(self):
        self.fill(0)
        self.show()
        # DEBUG close self.display ?

    def clear(self):
        self.fill(0)
        self.show()

    def print(self, text, x=0, y=0):
        """Print some text to the display.
        """
        print("*** ", text, " ***")
        # Wrap lines at newlines :
        folded_text = text.split("\n")
        # Rewrap at line length :
        line_list = []
        for line in folded_text:
            for index in range(len(line) // self.SCREEN_LENGTH + 1):
                line_list.append(
                        line[ self.SCREEN_LENGTH*index : self.SCREEN_LENGTH*(index+1) ]
                )
        self.clear()
        for index, line in enumerate(line_list):
            # index starts at 0.
            if index >= self.SCREEN_HEIGHT:
                # Do not raise an error, but warn on stdout
                print('! only %i chars in OLED display ; couldn\'t print :\n"%s"' %
                        (self.SCREEN_LENGTH * self.SCREEN_HEIGHT, line))
            self.text(line, x, y + index*self.CHAR_SIZE)
        self.show()

    def draw_pixel(x, y):
        """Set a pixel on. provided x is below WIDTH, y below HEIGHT.
        """
        self.pixel(x, y, 1)
        self.show()

    def draw_vline(x, y, h):
        """Draw a vertical line, starting from (x, y), h pixels high.
        """
        self.vline(x, y, h, 1)
        self.show()

    def draw_hline(x, y, w):
        """Draw a horizontal line, starting from (x, y), w pixels wide.
        """
        self.hline(x, y, w, 1)
        self.show()


class _OLEDDisplayEsp32(_OLEDDisplay):
    """Implement ESP32 OLED display
    """
    TXD1_PIN = 4                        # OLED_SDA
    SDA_PIN = 16                        # OLED_RST
    CLK_PIN = 15                        # OLED_SCL

    def __init__(self):
        import esp32
        super().__init__()


class _OLEDDisplayEsp8266(_OLEDDisplay):
    """Implement TTGO ESP8266 OLED display
    """
    TXD1_PIN = 2                        # OLED_SDA
    SDA_PIN = 4                         # OLED_RST
    CLK_PIN = 14                        # OLED_SCL

