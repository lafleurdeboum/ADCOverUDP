import sys
import machine
import time


class ADC(machine.ADC):
    """superseed micropython's ADC class, hiding platform details.
    """

    if sys.platform == "esp32":
        #import esp32
        ADC_PIN = 32
        # esp32 ADC outputs an int up to 4096. It is reputated not reliable on its
        # first 10%, so we'll use an according FLOOR read value :
        FLOOR = b"410"
        #self.adc.width(machine.ADC.WIDTH_9BIT)
    elif sys.platform == "esp8266":
        # esp8266 ADC outputs 1024 levels. Same remarks apply.
        FLOOR = b"102"
    elif sys.platform == "linux":
        # We will use a dummy ADC defined in machine.py
        FLOOR = b"410"

    def __init__(self):
        if sys.platform == "esp32":
            super().__init__(machine.Pin(self.ADC_PIN))
            self.atten(machine.ADC.ATTN_11DB)
            self.width(machine.ADC.WIDTH_9BIT)
        elif sys.platform == "esp8266":
            super().__init__(0)
        elif sys.platform == "linux":
            super().__init__(machine.Pin(0))

    def readMeaningfulValue(self):
        """Blocking call looping on the ADC until it reaches ADC.FLOOR
        (machine-specific sensible noise filter).
        """
        readValue = 0
        while int(readValue) < int(ADC.FLOOR):
            self.takeASmallNap()
            readValue = self.read()
        print(readValue)
        #return b"%04i" % readValue
        return readValue

    def takeASmallNap(self):
        """Hang 500 microseconds.
        """
        time.sleep(0.0005)



