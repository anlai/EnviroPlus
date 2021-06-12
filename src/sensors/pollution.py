#!/usr/bin/env python3

import logging
import aqi
from pms5003 import PMS5003, ReadTimeoutError
import settings

# initialize the sensor
pms5003 = PMS5003()

# calculates the epa AQI value
# Based off of the chart here: https://www.airnow.gov/aqi/aqi-basics/
def calculate_aqi(pm25, pm10):
    aqi_val = aqi.to_aqi([
        (aqi.POLLUTANT_PM25, pm25),
        (aqi.POLLUTANT_PM10, pm10)
    ])
    aqi_cat = 'Unknown'
    if 0 <= aqi_val <= 50:
        aqi_cat = 'Good'
    elif 51 <= aqi_val <= 100:
        aqi_cat = 'Moderate'
    elif 101 <= aqi_val <= 150:
        aqi_cat = 'Unhealthy for Sensitive Groups'
    elif 151 <= aqi_val <= 200:
        aqi_cat = 'Unhealthy'
    elif 201 <= aqi_val <= 300:
        aqi_cat = 'Very Unhealthy'
    elif 301 <= aqi_val <= 500:
        aqi_cat = 'Hazardous'
    else:
        aqi_cat = 'Unknown'

    return {
        "aqi-val": aqi_val,
        "aqi": aqi_cat
    }

# get particulate matter data
def get_reading():
    readings = pms5003.read()

    if settings.VERBOSE:
        logging.info(f'pm 2.5: {readings.pm_ug_per_m3(2.5)}')
        logging.info(f'pm 10: {readings.pm_ug_per_m3(10)}')
        logging.info(f'pm 1: {readings.pm_ug_per_m3(1)}')
        logging.info(f'aqi: {calculate_aqi( readings.pm_ug_per_m3(2.5), readings.pm_ug_per_m3(10))}')

    return {
        "pm2.5": readings.pm_ug_per_m3(2.5),
        "pm10": readings.pm_ug_per_m3(10),
        "pm1": readings.pm_ug_per_m3(1),
        "aqi": calculate_aqi( readings.pm_ug_per_m3(2.5), readings.pm_ug_per_m3(10))
    }