# Scripted Setup

This method for setting up the tool is really just all the commands you need to run in order to install and setup the software.  Assumption is that you've already run the basic setup outlined on the README.

1. Install Prereqs

```bash
sudo apt install -y git python3-pip
git clone https://github.com/pimoroni/enviroplus-python.git ~/enviroplus-python
sudo ~/enviroplus-python/install.sh
```

2. Install the Application

```bash
git clone https://github.com/anlai/EnviroPlus.git ~/enviroplus
pip3 install -r ~/enviroplus/setup/requirements.txt
chown -R pi:pi ~/enviroplus/src
```

3. Configure InfluxDB Connections

Create a file in `~/enviroplus/src/config.ini`, with the following contents and the tokens replaced with your server information (completely replace the curly braces).

```
[influx2]
url=https://{{ influxdb.host }}:{{ influxdb.port }}
org={{ influxdb.org }}
token={{ influxdb.token }}
timeout=6000
```

4. Update settings.py

Update the file `~/enviroplus/src/settings.py`.  Replace the values `INFLUX_BUCKET` and `INFLUX_ORG` with values specific to your Influx install.

5. Setup as a Service

Create a new file `/etc/systemd/system/envplus.service`

```
[Unit]
Description=Enviroplus Collector
After=network.target

[Service]
User=pi
Group=pi
WorkingDirectory=/home/pi/enviroplus/src
ExecStart=python3 /home/pi/enviroplus/src/envplus.py
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
```

Run the following commands:

```bash
sudo chmod 0644 /etc/systemd/system/envplus.service
sudo systemctl daemon-reload
sudo systemctl start envplus
sudo systemctl status envplus
sudo systemctl enable envplus
```