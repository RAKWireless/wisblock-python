#!/usr/bin/env python3
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas

import sys
import threading
import netifaces
import psutil


def cb():

	info = ""
	#get interface ipv4 address
	ifaces = netifaces.interfaces()

	if 'eth0' in ifaces:
		eth0 = netifaces.ifaddresses('eth0')
		ipv4 = eth0.get(netifaces.AF_INET)

		if ipv4 != None:
			addr = ipv4[0]['addr'] 
			info += "IP:%s\n"%addr

	if 'eth1' in ifaces:
		eth1 = netifaces.ifaddresses('eth1')
		ipv4 = eth1.get(netifaces.AF_INET)

		if ipv4 != None:
			addr = ipv4[0]['addr']
			info += "IP:%s\n"%addr
	
	if 'wlan0' in ifaces:
		wlan0 = netifaces.ifaddresses('wlan0')
		ipv4 = wlan0.get(netifaces.AF_INET)

		if ipv4 != None:
			addr = ipv4[0]['addr']
			info += "IP:%s\n"%addr
	
	#get cpu percent
	cpu = psutil.cpu_percent(None)
	info += "CPU:%.1f"%cpu
	info += "%\n"
 
	#get free memory percent
	memory = 100 - psutil.virtual_memory().percent
	info += "Free Mem:%.1f"%memory
	info += "%\n"
	
	#print information to dispaly
	with canvas(device) as draw:
		draw.text((0, 0), info, fill="white", spacing=2)

	timer = threading.Timer(1, cb)
	timer.start()


try:
    serial = i2c(port=1, address=0x3c)
    device = ssd1306(serial)
except Exception:
    print("can not find oled device.")
    sys.exit()

timer = threading.Timer(1, cb)
timer.start()


