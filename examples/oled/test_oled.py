#!/usr/bin/env python3
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas

import sys
import threading
import netifaces
import psutil
import re
import subprocess

def cb():

    info = ""
    pattern = "^bond.*|^[ewr].*|^br.*|^lt.*|^umts.*|^lan.*"

    #get all interfaces
    ifaces = netifaces.interfaces()

    #get bridge interfaces created by docker 
    p = subprocess.run('docker network ls -f driver=bridge --format "br-{{.ID}}"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    br_docker_ifaces = p.stdout.decode()
    
    for iface in ifaces:
        # match only interface names starting with e (Ethernet), br (bridge), w (wireless), r (some Ralink drivers use>
        # get rid off of the br interface created by docker
        if re.match(pattern, iface) and iface not in br_docker_ifaces:
                
            ifaddres = netifaces.ifaddresses(iface)
            ipv4 = ifaddres.get(netifaces.AF_INET)
            if ipv4:
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


