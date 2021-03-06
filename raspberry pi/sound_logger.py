import os
import time
import serial
import sys
import json
import subprocess
from json import dumps, load
from time import gmtime, strftime
from subprocess import call

serialport = serial.Serial('/dev/ttyAMA0', 9600, parity=serial.PARITY_EVEN, timeout=1)

previous_val = 0;
first = True


def ByteToHex( byteStr ):
  return ''.join( [ "%02X" % x for x in byteStr ] ).strip()

def InitDevice( ):
  serialport.write('\x10\x04\x0d')
	
  result = bytearray()

  while True:	
    byte = serialport.read(1)
    if not byte: break
    
    for x in byte:
      result.append(x)
  
  if(len(result) == 0):
    return False

  return True


def WriteData( val_str ):
    filename = strftime("/var/www/data/%m%d%Y.tsv", time.localtime())
    if(os.path.exists(filename) == False):
      with open(filename, 'a+') as f:
        f.write("Time\tdBA\n")

    try:
      with open(filename, 'a+') as f:
        timestamp = strftime("%m-%d-%Y %H:%M:%S", time.localtime())
	f.write(timestamp + "\t" + val_str + "\n")
    except:
      raise

    return
      
if(InitDevice() == False):
    print "unable to open device"
    exit(0)
	  

while 1:  
	result = bytearray()
	serialport.write('\x30\x00\x0d')
 
	while True: 
		  
	  byte = serialport.read(1)
	  if not byte: break

	  for x in byte:
	    result.append(x)

        if(len(result) == 0): 
	  continue

	# A/C
	ac = (result[0] & (1 << 7)) >> 7
	#print('A ' if ac == 0 else 'C, ' )

	# Slow/Fast
	sl = (result[0] & (1 << 3)) >> 3
	#print('Fast, ' if sl == 0 else 'Slow, ')

	# Level
	factor = (result[0] & ((1 << 5) | (1 << 4))) >> 4
	sys.stdout.write('Level: %d ' % (40 + (int(bin(factor), 2) * 20)))

	# Value
	val = ((result[0] & 0x7) << 8) | result[1]
	tmp_str = '%d' % val
	val_str = tmp_str[:-1] + '.' + tmp_str[-1:]
	sys.stdout.write(val_str + " dB \r")
	sys.stdout.flush()

	WriteData(val_str)
		
s.close()


