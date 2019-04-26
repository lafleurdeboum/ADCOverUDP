import gc
import array
import machine
import time
import sys
if sys.platform == "esp32":
    import esp32
    ADC_PIN = 32
    ADC = machine.ADC(machine.Pin(ADC_PIN))
    ADC.atten(machine.ADC.ATTN_11DB)
    READ_MIN = 400
    #self.adc.width(machine.ADC.WIDTH_9BIT)
elif sys.platform == "esp8266":
    ADC = machine.ADC(0)
    READ_MIN = 6
elif sys.platform == "linux":
    import random
    def ADC():
        """fake ADC to let you run the code on computers"""
        time.sleep(random.randint(0, 9))
        return random.randint(410, 4095)

import network_helpers
import Display

# _print to OLED GPIO display if any, otherwise
# default to stdout :
_print = Display.Display().Dprint

def pause():
    """Hang a few milliseconds"""
    #machine.sleep(0.01)
    #machine.lightsleep(10)
    machine.idle()
    time.sleep_ms(10)

def read_adc():
    read_value = 0
    while read_value < READ_MIN:
        pause()
        read_value = ADC.read()
    print(read_value)
    return b"%04i" % read_value

def main():
    _print("Connecting wifi")
    #nic = network_helpers.setup_wifi()
    nic, broadcast = network_helpers.setup_ap()
    while not nic.isconnected():
        pause()

    print("broadcast is %s" % broadcast)

    sock = network_helpers.setup_socket(nic)
    address = (broadcast, network_helpers.PORT)
    then = time.time()
    count = 0
    while True:
        _print("Sending ADC signal to\n%s\nport %s" %
                address)
        while nic.isconnected():
            try:
                sock.sendto(read_adc(), address)
                count += 1
            except OSError:
                _print(count)
                raise
            except KeyboardInterrupt:
                _print(count)
                raise
            pause()
            if time.time() - then > 1:
                #_print("#%i - %i space" % (count, gc.mem_free()))
                gc.collect()
                then += 1

        _print("Awaiting conn on AP\n%s" % nic.config("essid"))
        while not nic.isconnected():
                pause()


if __name__ == "__main__":
    main()

