# Ansible Setup

This method uses Ansible scripts to fully configure the Pi.  However in testing I have experienced some issues with the apt steps hanging.  The [hybrid method](Hybrid-Setup.md) might be the best of both worlds for now but it's not ideal.

The playbook has been tested to run on a Ubuntu 20.04 WSL container.

1. Clone this repository to your Ansible server (assumed to be cloned to ~/enviro)
2. Configure your secrets/settings in `~/enviro/src/main.yml`

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

3. Update Ansible Inventory

Add list of hosts into the `~/enviro/setup/inventory` under the `[airquality]` tag.

4. Initial Install

Execute this to do a full setup (intalling packages and everything).  If you've already run it to completion, you can probably just do step 5.

```bash
cd ~/enviro/setup
ansible-playbook -i ./inventory ./main.yml --extra-vars "{initial_install: yes}" -vv
```

5. App Update

Run this for just doing app deployments (saves time) when you don't need to do the package installs, just for either updating the application or changing a setting in step 2.

```bash
cd ~/enviro/setup
ansible-playbook -i ./inventory ./main.yml -vv
```