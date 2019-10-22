# Botton!
Our precious, one botton to rule them all.

## Setup

The Botton should run on a Raspberry Pi which has the following set up:

1. The user `botton` added
2. The default user `pi` disabled or removed
3. Install dependencies by running `sudo apt-get install python-pip python-smbus python-rpi.gpio i2c-tools`
4. This repo should be in `/home/botton/botton` (you can't clone it from ghe.spotify.net though since the Raspberry won't have access - push it to the Raspberry by using scp or something instead)
5. To go the folder and run `pip install -r requirements.txt`
6. Copy [`botton.conf`](conf/supervisord/botton.conf) to `/etc/supervisor/conf.d/botton.conf`
7. Run `sudo supervisorctl start botton`

## Run

By adding the supervisord conf file Botton should start automatically. You can use the following commands to start/stop it though:

#### Start
`sudo supervisorctl start botton`

#### Stop
`sudo supervisorctl stop botton`

## Logs
The log can be found here: `/var/log/botton.log`

## Debugging

You can use the switches on the Botton box to interface with debugging features (but only when in the logged out state):

### Restart app
Restart the app (will call `supervisorctl restart botton`) by:

1. Pull lower (PR) switch to the right five times

### View IP address
Make the LCD display show the current IP of the Botton Raspberry Pi box:

1. Pull upper (repo) switch to the right two times
2. Pull lower (PR) switch to the left two times

To hide the IP flip any of the switches once
