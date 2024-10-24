#!/usr/bin/python3
import os
import time
import math
import random

from dotenv import load_dotenv
import robin_stocks.robinhood as rh

import rainbowhat
from scroll import scroll_number

# constants
MAX_BRIGHTNESS = .1
FULL_SCALE_PERCENT = 10 # an X% change will fill the rainbow

CRYPTO_LIST = ['DOGE']

# get Robinhood username and password from .env
load_dotenv()

RH_USERNAME = os.getenv("RH_USERNAME")
RH_PASSWORD = os.getenv("RH_PASSWORD")

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

# login to robinhood
login = rh.login(RH_USERNAME, RH_PASSWORD)

if not login:
    print("login failed")
    exit(1)

#cryptos = rh.crypto.get_crypto_positions()
#print(cryptos)

try:
    while running:

        for ticker in CRYPTO_LIST:
            rainbowhat.display.clear()
            rainbowhat.display.print_str(ticker, justify_right=False)
            rainbowhat.display.show()

            doge = rh.crypto.get_crypto_quote(ticker)

            open_price = float(doge['open_price'])
            mark_price = float(doge['mark_price'])

            if open_price > 0.0: # error check
                hang_out(2)

                crypto_change = mark_price - open_price
                crypto_change_percent = crypto_change / open_price

                r = 0
                g = 0
                b = 0

                if crypto_change > 0.0:
                    g = 1
                else:
                    r = 1

                rainbowhat.rainbow.clear()

                scaled_percent = min(1.0,abs((crypto_change_percent * 100.0) / FULL_SCALE_PERCENT))
                pixels = round(7 * scaled_percent)

                for x in range(pixels):
                    if crypto_change > 0.0:
                        pixel = 6 - x
                    else:
                        pixel = x

                    rainbowhat.rainbow.set_pixel(pixel,int(r*255),int(g*255),0,.1)

                print('Ticker: {}, Open: {:0.4f}, Market: {:0.4f}, change: {:0.4f}, percent: {:0.2f}%, scaled: {:0.2f}%, pixels: {}'.format(
                    ticker, 
                    open_price, 
                    mark_price, 
                    crypto_change, 
                    crypto_change_percent * 100.0, 
                    scaled_percent * 100.0, 
                    pixels))

#                rainbowhat.display.clear()
#                rainbowhat.display.print_number_str('{:0.3f}'.format(mark_price), justify_right=False)
#                rainbowhat.display.show()
                rainbowhat.rainbow.show()
                scroll_number('{:0.3f}'.format(mark_price))

                hang_out(60)
        
            else:
                rainbowhat.display.print_str("DATA")
                rainbowhat.display.show()
                hang_out(60)

except KeyboardInterrupt:
    pass

rainbowhat.display.clear()
rainbowhat.display.show()

exit(0)

