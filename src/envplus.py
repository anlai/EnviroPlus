#!/usr/bin/env python3

import sys
import logging
import time
import platform
import queue

import settings
from sensors import ambient, pollution
import target
import display

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logging.info("""Enviro+ InfluxDB Collector
Press Ctrl+C to exit!
""")

def main():

    statusHistory = []

    while True:

        if len(statusHistory) > 4:
            statusHistory.pop(0)

        try:
            # retrieve the values
            amb = ambient.get_reading()
            pol = pollution.get_reading()

            # push data to target
            target.pushData(platform.node(),amb,pol)

            statusHistory.append(True)

            # update the display
            display.update(amb,pol,statusHistory)

            time.sleep(settings.INTERVAL)
        
        # Exit cleanly
        except KeyboardInterrupt:
            sys.exit(0)

        except:
            logging.info(f"ERROR: {sys.exc_info()[0]}")
            statusHistory.append(False)
            pass

        logging.info(f"Status History: {statusHistory}")


if __name__ == "__main__":
    main()