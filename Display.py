"""OLED display driver

The special function Display returns a new instance of a useful _Display class. 
If running on esp32 or esp8266, it will try to write to an i2c connected OLED 
display. If running on any other platform, it will emulate this by printing
things to stdout, like in

*** a thing ***

tested and proved with https://www.aliexpress.com/item/Lolin-ESP32-OLED-V2-0-Pro-ESP32-OLED-wemos-pour-Arduino-ESP32-OLED-WiFi-Modules-Bluetooth/32824819112.html

tested and proved with https://www.ebay.fr/itm/Wemos-TTGO-ESP8266-0-91-Inch-OLED-For-Arduino-Nodemcu/142834378288?hash=item214197a630:g:cQQAAOSwAC1aH~mr:rk:48:pf:0

using https://www.pymadethis.com/article/oled-displays-i2c-micropython/
and connection pins referenced in http://simplestuffmatters.com/wemos-ttgo-esp8266-with-0-91-inch-oled/
"""


def Display():
    try: d = _DisplayEsp32()
    except ImportError:
        try: d = _DisplayEsp8266()
        except ImportError:
            d = _DisplayX86()
    return d


class _DisplayX86:
    """Emulate OLED display. This lets you run the package on computers
    """
    arch = "x86"
    def print(self, arg):
        print("*** ", arg, " ***")


class _OledDisplay:
    """The real Oled display manager

    self.display.pixel function would output value if we omit c=1 (on) or 0 (off)
    """
    def __init__(self):
        from machine import I2C, Pin, reset
        import ssd1306
        import time
        led_reset_pin = Pin(self.SDA_PIN, Pin.OUT)
        led_reset_pin.off()
        time.sleep(0.1)
        led_reset_pin.on()
        time.sleep(0.1)
        i2c = I2C(scl=Pin(self.CLK_PIN), sda=Pin(self.TXD1_PIN), freq=100000)
        self.display = ssd1306.SSD1306_I2C(128, 32, i2c)

    def close(self):
        self.display.fill(0)
        self.display.show()
        # DEBUG close self.display ?

    def clear(self):
        self.display.fill(0)
        self.display.show()

    def print(self, text, x=0, y=0):
        """Print some text. A char is roughly 8 pixels high and 4 wide."""
        #global line_length, screen_height, char_height
        # Wrap lines at newlines :
        folded_text = text.split("\n")
        # Rewrap at line length :
        line_list = []
        for line in folded_text:
            for index in range(len(line) // self.line_length + 1):
                line_list.append(
                        line[ self.line_length*index : self.line_length*(index+1) ]
                )
        self.clear()
        for index, line in enumerate(line_list):
            # index starts at 0.
            if index >= self.screen_height:
                # The error gets raised only after first lines are printed :
                    raise OSError("only %i chars in OLED display ; couldn't print : %s" %
                        (self.line_length * self.screen_height, line))
            self.display.text(line, x, y + index*self.char_height)
        self.display.show()

    def get_pixel(x, y):
        """get the color at pixel (value from 0 to 1)"""
        return self.display.pixel(x, y)

    def draw_pixel(x, y):
        """Set a pixel on. x is below 128, y below 32"""
        self.display.pixel(x, y, 1)
        self.display.show()

    def draw_vline(x, y, h):
        """Draw a vertical line, starting from (x, y), h pixels high"""
        self.display.vline(x, y, h, 1)
        self.display.show()

    def draw_hline(x, y, w):
        """Draw a horizontal line, starting from (x, y), w pixels wide"""
        self.display.hline(x, y, w, 1)
        self.display.show()


class _DisplayEsp32(_OledDisplay):
    """Implement ESP32 OLED display
    """
    arch = "Esp32"
    TXD1_PIN = 4            # OLED_SDA
    SDA_PIN = 16            # OLED_RST
    CLK_PIN = 15            # OLED_SCL
    line_length = 16        # OLED char per line
    screen_height = 4       # OLED char per column
    char_height = 8         # OLED font char height

    def __init__(self):
        import esp32
        super().__init__()


class _DisplayEsp8266(_OledDisplay):
    """Implement TTGO ESP8266 OLED display
    """
    arch = "Esp8266"
    TXD1_PIN = 2            # OLED_SDA
    SDA_PIN = 4             # OLED_RST
    CLK_PIN = 14            # OLED_SCL
    line_length = 16        # OLED char per line
    screen_height = 3       # OLED char per column
    char_height = 8         # OLED font char height


if __name__ == "__main__":
    display = Display()
    display.print("Hurray !")

