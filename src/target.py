#!/usr/bin/env python3

import settings
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# initialize influxdb client
client = InfluxDBClient.from_config_file(settings.INFLUX_CONFIG_PATH)
write_api = client.write_api(write_options=SYNCHRONOUS)

def pushData(nodeName,amb,pol):
    points = [{ 
        "measurement": "enviroplus",
        "tags": { 'sensor': nodeName },
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

    write_api.write(settings.INFLUX_BUCKET, settings.INFLUX_ORG, points)