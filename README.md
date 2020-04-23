# CompuLinkBridge
Control your compulink enabled devices from a raspberry pi with bluetooth input

## Requirements
raspberry pi with bluetooth, 3b+ or better

python 2.7 (default in raspbian)

evdev - pip install evdev

## Installation:
Download zip file or use git: `git clone https://github.com/andrewzirkel/CompuLinkBridge.git`

Add `python <path to>/compulinkbridge.py &` to /etc/rc.local

## Other Notes
The only device type supported is CD Player.  You can easily add what need in the keycode_compulink_map dictionary in harmony.py

## Utilities
`compulinkbridgesendcommand.py -a <address(1-15)> -c <command(0-15)>`

`compulinkMapper.py` - Send sequential addresses and commands to the compulink bus so one can observe the affects on a device.

## Disclaimer
This software is offered for free use without any warranty.  It may damage your equipment and/or media.  Your cd may get scratched and your tapes may get broken.
