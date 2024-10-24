#!/usr/bin/python3
import time
import json
import urllib.request

import rainbowhat

# constants
MAX_BRIGHTNESS = .1
MAX_KP = 10

KP_JSON = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"

running = True

@rainbowhat.touch.C.press()
def touch_c(channel):
    print("Key C pressed... exiting...")

    rainbowhat.display.print_str('EXIT')
    rainbowhat.display.show()

    global running
    running = False

# sleep for duration seconds, but let handlers happen
def hang_out(duration):
    for x in range(duration):
        if not running:
            break
        time.sleep(1)

try:
    while running:

        rainbowhat.display.clear()
        rainbowhat.display.print_str("LOAD")
        rainbowhat.display.show()

        with urllib.request.urlopen(KP_JSON) as url:
            data = json.load(url)
            #print(data[-1])
        latest = data[-1]

        r = 0
        g = 0
        b = 0

        kp = latest['kp_index']
        rainbowhat.display.clear()
        rainbowhat.display.print_number_str('{:0.1f}'.format(latest['estimated_kp']))
        rainbowhat.display.show()

        if kp < 4:
            g = 1
        else:
            r = 1

        rainbowhat.rainbow.clear()

        pixels = round(7 * (kp / MAX_KP))

        for pixel in range(pixels):
            rainbowhat.rainbow.set_pixel(6-pixel,int(r*255),int(g*255),0,.1)

#                rainbowhat.display.clear()
#                rainbowhat.display.print_number_str('{:0.3f}'.format(mark_price), justify_right=False)
#                rainbowhat.display.show()
        rainbowhat.rainbow.show()
        hang_out(60)

except KeyboardInterrupt:
    pass

rainbowhat.display.clear()
rainbowhat.display.show()

exit(0)

