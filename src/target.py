#!/usr/bin/env python3

import settings
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# initialize influxdb client
client = InfluxDBClient.from_config_file(settings.INFLUX_CONFIG_PATH)
write_api = client.write_api(write_options=SYNCHRONOUS)

def pushPoints(points):
    write_api.write(settings.INFLUX_BUCKET, settings.INFLUX_ORG, points)