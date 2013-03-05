#!/usr/bin/env python

import sys
import telnetlib
import subprocess
import signal
import time

###############################################################
# This script will automatically flash and start a GDB debug 
# session to the STM32 discovery board using OpenOCD. It is
# meant to be called from the rake task "debug" (execute 
# rake debug) and the working directory is assumed to be the
# project root
###############################################################

###############################################################
# Set up an override to send a ctrl-c to GDB
###############################################################
def signal_handler(signal, frame):
    # Close down openocd
    open_ocd.terminate()
    open_ocd.wait()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

###############################################################
# Start up openocd in the background
###############################################################
open_ocd = subprocess.Popen(["openocd"])

time.sleep(2) # Wait for this to start up

###############################################################
# Flash the new image to the development board
###############################################################

# Create the flashable image
create_flash = subprocess.Popen(["arm-none-eabi-objcopy", "-Obinary", "build/artifacts/release/flash.elf", "build/artifacts/release/flash.bin"])
create_flash.wait()

# Flash the image
tn = telnetlib.Telnet("127.0.0.1", "4444")
tn.read_until("> ")
tn.write("poll\n")
tn.read_until("> ")
tn.write("reset halt\n")
tn.read_until("> ")
tn.write("flash probe 0\n")
tn.read_until("> ")
tn.write("flash write_image erase build/artifacts/release/flash.bin 0x08000000\n")
tn.read_until("> ")
tn.write("reset\n")
tn.read_until("> ")
tn.write("exit\n")
tn.close()

###############################################################
# Start the gdb session
###############################################################

#time.sleep(2)
#gdb_proc = subprocess.Popen(["arm-none-eabi-gdb", "-ex", "target remote localhost:3333", "build/artifacts/release/flash.elf", "-ex", "set remote hardware-breakpoint-limit 6", "-ex", "set remote hardware-watchpoint-limit 4", "-ex", "cont"])
#time.sleep(1)
#gdb_proc.send_signal(signal.SIGINT)
print "\nRun the following command in another terminal to start the GDB session"
print "arm-none-eabi-gdb -ex \"target remote localhost:3333\" -ex \"set remote hardware-breakpoint-limit 6\" -ex \"set remote hardware-watchpoint-limit 4\" build/artifacts/release/flash.elf"

print "\nPress ctrl-c to exit"

signal.pause() # Wait forever

