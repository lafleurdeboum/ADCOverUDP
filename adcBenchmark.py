import time
import machine
import hardware


flag = False
#_print = hardware.Display().print
adc = hardware.ADC()

def timeADC():
    retries = 100
    start = time.ticks_us()

    for i in range(retries):
        _ = adc.read()

    duration = time.ticks_diff(time.ticks_us(), start)
    print("sampling period : %s useconds" % str(duration / retries))
    # on esp8266, gives around 225 useconds.
    # on esp32, 70 us.

def testSoundLength():
    read_value = getADCtrigger(floor)
    start = time.ticks_us()
    _ = adc.readMeaningfulValue()
    duration = time.ticks_diff(time.ticks_us(), start)
    print("signal length : %i useconds" % duration)
    print("\t(%i samples)" % i)


if __name__ == "__main__":
    print("benchmarking the ADC's samplerate ...")
    timeADC()
    print("Please feed ADC, testing signal length ...")
    testSoundLength()

