#!/usr/bin/env python3

import logging
from bme280 import BME280
from gpiozero import CPUTemperature
from enviroplus import gas
from enviroplus.noise import Noise
import settings

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

# initialize the sensors
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)
noise = Noise()

# Create array for averages
gas_array = []
cpu_temps = []

# get ambient temp
def get_temp():
    global cpu_temps

    # factor base from pimoroni exampls
    factor = settings.TEMP_FACTOR #1.2

    # retrieve cpu temps
    cpu_temp = get_cputemp()
    cpu_temps.append(cpu_temp)
    avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))

    # retrieve the temp
    raw_temp = bme280.get_temperature()

    # compensate
    comp_temp = raw_temp - ((avg_cpu_temp - raw_temp) / factor)

    if settings.VERBOSE:
        logging.info(f'comptemp: {convert_temptoF(comp_temp)}')
        logging.info(f'raw temp: {convert_temptoF(raw_temp)}')
        logging.info(f'cpu temp: {convert_temptoF(cpu_temp)}')

    # Clean up Array so it doesn't overflow memory
    if (len(cpu_temps) > 10):
        cpu_temps.pop(0)

    return convert_temptoF(comp_temp)

# get cpu temp
def get_cputemp():
    temp = CPUTemperature().temperature
    if settings.VERBOSE:
        logging.info(f'cpu Temp: {temp}')
    return temp

# convert celsius to fahrenheit
def convert_temptoF(celsiusTemp):
    return round(celsiusTemp * 1.8 + 32)

# get the humidity
def get_humidity():
    humidity = bme280.get_humidity()
    if settings.VERBOSE:
        logging.info(f'humidity: {humidity}')
    return humidity

# get the pressure
def get_pressure():
    pressure = bme280.get_pressure()
    if settings.VERBOSE:
        logging.info(f'pressure: {pressure}')
    return pressure

# get carbon monoxide
def get_gas():
    global gas_array

    # Get Gas
    gas_reading = gas.read_all()
    gas_array.append(gas_reading.reducing)
    # If the array is larger than 8 items dump the first one
    if (len(gas_array) > 8):
        gas_array.pop(0)

    gas_average = (sum(gas_array) / len(gas_array))
    gas_warning = (gas_reading.reducing > (gas_average * 1.05)) and (len(gas_array) == 8)

    if settings.VERBOSE:
        logging.info('carbon monoxide raw: {gas_reading.reducing}')
        logging.info('carbon monoxide avg: {gas_average}')
        logging.info('carbon monoxide warn: {gas_warning}')

    return {
        "gas_avg": gas_average,
        "gas_warning": gas_warning,
        "gas_reducing": gas_reading.reducing,
    }

# gets the noise level in db
def get_noise():
    noise_amount = noise.get_amplitude_at_frequency_range(20, 8000)
    if settings.VERBOSE:
        logging.info(f'noise: {noise_amount}')
    return int(round(noise_amount * 100))

# gets all the weather parameters
def get_reading():
    gasvalues = get_gas()

    return {
        "temp": get_temp(),
        "cpu_temp": get_cputemp(),
        "humidity": get_humidity(),
        "pressure": get_pressure(),
        "carbon_monoxide": gasvalues['gas_reducing'],
        "carbon_monoxide_warning": gasvalues['gas_warning'],
        "noise": get_noise()
    }