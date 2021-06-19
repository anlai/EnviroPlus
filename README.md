
This is still a work in progress, but the python code is mostly there.

# Enviro+ Data Collector

This code heavily borrowed from the Pimoroni examples on how to collect and display the data.  It collects data from the suite of environmental sensors when using a Pimoroni Enviro+ and PMS5003.  You can do a couple of things with the information: display it on the screen, push it to InfluxDB, or override the InfluxDB target to your choice of target.

## Required Hardware

- Raspberry Pi Zero WH
- Pimoroni Enviro+ Board
- PMS5003 Particle Sensor

The above components are required just for the software to work, but if you want to make it in a nice case you can check out my [case design here](https://github.com/anlai/EnviroPlus_Case).

## Setup

There are two ways to setup the Pi, if you are doing more than one I would recommend the Ansible playbook.  But either way you'll want to configure the Pi for headless configuration [instructions here](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md).  As well as enabling ssh by creating an empty file named `ssh` in the root of the sd card.

### Manual Steps

Both methods below require these steps done first, these are the final configuration steps so everything else can be done.  Once you have it booted up and connected to your wifi, you need to configure a few items:

- open `raspi-config`
  - set the password for the pi user
  - set the hostname (this will get used as a tag in the data)
  - expand the file system
- pull in your SSH certificate
- run apt update and upgrade

### Ansible

To execute the Ansible playbook, I recommend running it from a different computer (eg. a Linux box or Windows WSL instance) this way if you have multiple to setup you can just configure your inventory and have them all provisioned and updated easily.

First thing you'll need to do is clone this repository locally, we'll assume the repo is cloned to `~/enviro`.  So if you don't put it there, just replace that with your location.  Once it's cloned, you have a few configuration settings to change in order for it to configure them properly.

Open up `~/enviro/setup/main.yml` in your favorite editor.  There are a few variables to update in the vars section, see the table below for what belongs:

| Variable | Description |
| --- | --- |
| temp_factor | Adjustment factor for the temperature readings since the CPU temp throws off the ambient temperature reading |
| influxdb_bucket | InfluxDB bucket to send data to |
| city | Astral city to determine timezone and drives the color/design of the background |
| time_zone | Time zone you would like the time adjusted to |
| influxdb.host | Host to your influxdb |
| influxdb.port | Port of your influxdb |
| influxdb.org | Org where your bucket resides in InfluxDB |
| influxdb.token | Authentication token for InfluxDB |

Next open the `~/enviro/setup/inventory` file and replace `REPLACE_ME_WITH_HOST_IP_FOR_PI` with your IP addresses to each environmental sensor (each on their own line).

Once the setup is completed you are ready to run the Ansible playbook and get your devices configured.  Execute the following commands from your Ansible computer:

```bash

```

### Scripts

## Configuration

## References

- Status Icons from:
  - [Font Awesome - Check Circle](https://fontawesome.com/v5.15/icons/check-circle?style=solid)
  - [Font Awesome - Times Circle](https://fontawesome.com/v5.15/icons/times-circle?style=solid)
- Air Quality Icons from:
  - [PM2.5](https://www.iconfinder.com/icons/7304531/pm2.5_dust_pollution_smog_dangerous_unhealthy_particulates_icon)