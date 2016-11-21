# AGPtek hdmi_extender

## v3.0:
just
```bash
vlc udp://@239.255.42.42:5004
```
if you have problems with the error `cannot join multicast group: No such device`
you just have to instruct your system which interface to use:
```bash
sudo route add -net 224.0.0.0 netmask 240.0.0.0 dev eth0
```
source: https://blog.danman.eu/new-version-of-lenkeng-hdmi-over-ip-extender-lkv373a/

## v1.0:
https://blog.danman.eu/reverse-engineering-lenkeng-hdmi-over-ip-extender/

usage: 
./hdmi_extender.py | vlc –
