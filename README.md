# Enviro+ Data Collector

This code heavily borrowed from the Pimoroni examples on how to collect and display the data.  It collects data from the suite of environmental sensors when using a Pimoroni Enviro+ and PMS5003.  You can do a couple of things with the information: display it on the screen, push it to InfluxDB, or override the InfluxDB target to your choice of target.

## Required Hardware

- Raspberry Pi Zero WH
- Pimoroni Enviro+ Board
- PMS5003 Particle Sensor

The above components are required just for the software to work, but if you want to make it in a nice case you can check out my [case design here](https://github.com/anlai/EnviroPlus_Case).

## Setup

There are a few different ways to set this up from scratch, but regardless of the method it should be setup for headless mode (unless you want to setup each one with keyboard and monitor attached)

Once you have the Pi booted up, you'll want to do some initial configuration.  Also probably want to pull down your ssh certificates.
```bash
echo "pi:{PASSWORD_HERE" | chpasswd
sudo raspi-config nonint do_hostname {HOST_NAME}
sudo raspi-config nonint do_expand_rootfs

sudo apt update && sudo apt upgrade -y
```
*Reference [here](https://gist.github.com/MkLHX/20a2a67c1dff747d73d48f2989ab2829)*

The 3 options to setup are:
1. [Ansible](Ansible-Setup.md)
2. [Scripts](Scripted-Setup.md)
3. [Hybrid of Ansible and Scripts](Hybrid-Setup.md)

## References

- [Pimoroni Python Examples](https://github.com/pimoroni/enviroplus-python)
- Status Icons from:
  - [Font Awesome - Check Circle](https://fontawesome.com/v5.15/icons/check-circle?style=solid)
  - [Font Awesome - Times Circle](https://fontawesome.com/v5.15/icons/times-circle?style=solid)
- Air Quality Icons from:
  - [PM2.5](https://www.iconfinder.com/icons/7304531/pm2.5_dust_pollution_smog_dangerous_unhealthy_particulates_icon)
  - [Pollution](https://www.iconfinder.com/icons/7304539/aerosol_air_spray_spread_dust_particulates_pollution_icon)