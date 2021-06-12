#!/usr/bin/env python3

import sys
import logging
import time
import platform

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

    try:
        while True:

            # retrieve the values
            amb = ambient.get_reading()
            pol = pollution.get_reading()

            # push data to target
            points = [{ 
                "measurement": "enviroplus",
                "tags": { 'sensor': platform.node() },
                "fields": {
                    "pm2_5": pol['pm2.5'],
                    "pm10": pol['pm10'],
                    "pm1": pol['pm1'],
                    "aqi_val": pol['aqi']['aqi-val'],
                    "aqi": pol['aqi']['aqi'],
                    "temp": amb['temp'],
                    "cpu_temp": amb['cpu_temp'],
                    "humidity": amb['humidity'],
                    "pressure": amb['pressure'],
                    "carbon_monoxide": amb['carbon_monoxide'],
                    "carbon_monoxide_warning": amb['carbon_monoxide_warning'],
                    "noise": amb['noise']
                }
            }]
            target.pushPoints(points)

            # update the display
            display.update(amb,pol)

            time.sleep(settings.INTERVAL)

    # Exit cleanly
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()