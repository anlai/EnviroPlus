# Hybrid Setup

Hybrid setup does the initial install steps from the [Scripted-Setup.md] and the app deployment from [Ansible-Setup.md].

The reason this exists is because Ansible sometimes hangs on some of the apt install steps and can potentially take multiple runs to complete.  It's not ideal but once you have your device(s) setup, making changes or updating is a breeze.

1. Install Prereqs (on the Pi)

```bash
sudo apt install -y git python3-pip
git clone https://github.com/pimoroni/enviroplus-python.git ~/enviroplus-python
sudo ~/enviroplus-python/install.sh
```

2. Run the Ansible Playbook (on the Ansible server)

Follow all the steps in [Ansible-Setup.md], except skip step 4.