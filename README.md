# ADCOverUDP.py

Send signals read from ADC over UDP broadcast (and use them).

## Audience

This was written for micropython on ESP boards. Porting to some other board
should be easy, one would need to modify `hardware.py` to suit specific
hardware parameter. The purpose is tested and succeeds on ESP32 and ESP8266
boards.

## Usage

Edit `board.py`. Copy files over to an ESP device serving as broadcaster 
(make sure to connect its ADC to something useful). Re-edit `board.py`. Upload
to the listener.

At the moment, the scripts rely on a working OLED display (to be changed).

