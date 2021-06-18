
This is still a work in progress, but the python code is mostly there.

# Enviro+ Data Collector

This code heavily borrowed from the Pimoroni examples on how to collect and display the data.  It collects data from the suite of environmental sensors when using a Pimoroni Enviro+ and PMS5003.  You can do a couple of things with the information: display it on the screen, push it to InfluxDB, or override the InfluxDB target to your choice of target.

## Required Hardware

- Raspberry Pi Zero WH
- Pimoroni Enviro+ Board
- PMS5003 Particle Sensor

The above components are required just for the software to work, but if you want to make it in a nice case you can check out my [case design here](https://github.com/anlai/EnviroPlus_Case).

## Setup

You can use the Ansible playbook to set up and deploy this but you'll need to do a couple of manual setup things first.  You'll want to configure the Pi for headless configuration [instructions here](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md).  As well as enabling ssh by creating an empty file named `ssh` in the root of the sd card.

Once you have it booted up and connected to your wifi, you need to configure a few items:
- open `raspi-config`
  - set the password for the pi user
  - set the hostname (this will get used as a tag in the data)
  - expand the file system
- (optional) pull in your SSH certificate
- run apt update and upgrade

## Configuration