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
if you have a very close setting of iptables there's something that needs to be changed,
for now I just disabled iptables with:

```bash
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT
```
this step needs to be troubleshooted

source: https://blog.danman.eu/new-version-of-lenkeng-hdmi-over-ip-extender-lkv373a/

## v1.0:
https://blog.danman.eu/reverse-engineering-lenkeng-hdmi-over-ip-extender/

usage: 
./hdmi_extender.py | vlc –

