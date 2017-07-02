import os
import time
import serial
import sys
import json
import subprocess
import datetime
from json import dumps, load
from time import gmtime, strftime
from subprocess import call
from datetime import timedelta
from datetime import datetime, date

serialport = serial.Serial('/dev/ttyAMA0', 9600, parity=serial.PARITY_EVEN, timeout=1)

previous_val = 20
running_mean = 0.0
samples = 0
last_recording = datetime.now()
last_sample = datetime.now()
recording_id = ""


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


def WriteData( val ):
    global recording_id
    global last_sample

    last_sample = datetime.now()
    recording_id = str(int(time.time()))

    localtime = time.localtime()

    dirpath = strftime("/var/www/data/%m%d%Y", localtime)
    if(os.path.exists(dirpath) == False):
      os.makedirs(dirpath)

    tmp_str = '%d' % val
    val_str = tmp_str[:-1] + '.' + tmp_str[-1:]  
    
    cap_str = ""

    if(val > 800):
      cap_str = recording_id
      CaptureImage(dirpath)


    filename = strftime(dirpath + "/data.tsv")
    if(os.path.exists(filename) == False):
      with open(filename, 'a+') as f:
        f.write("Time\tdBA\tinfo\n")

    with open(filename, 'a+') as f:
      timestamp = strftime("%m-%d-%Y %H:%M:%S", localtime)
      f.write(timestamp + "\t" + val_str + "\t" + cap_str + "\n")


    return
    
    
    
def CaptureImage(dirpath):
  global last_recording
  global recording_id
  
  if((datetime.now() - last_recording) < timedelta(seconds=5)):
    return
    
  call("sudo raspistill -t 5000 -tl 1000 -q 75 -w 640 -h 480 -o " dirpath + "/img/" + recording_id + "_%d.jpg -n", shell=True)
  last_recording = datetime.now()
  
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

  # Max Value
  if(val > max_val):
    max_val = val

  if(val > 800):
    writeData(val)

  if((datetime.now() - last_sample) > timedelta(seconds=10)):
    WriteData(max_val)
    max_val = 0 
  
  sys.stdout.write(str(val) + " dB max: " + str(max_val) + "\r")
  sys.stdout.flush()
  
  
s.close()

