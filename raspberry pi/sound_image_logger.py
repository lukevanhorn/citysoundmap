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


def WriteData( val_str ):
    global recording_id
    
    filename = strftime("/var/www/data/%m%d%Y.tsv", time.localtime())
    if(os.path.exists(filename) == False):
      with open(filename, 'a+') as f:
        f.write("Time\tdBA\tinfo\n")

    with open(filename, 'a+') as f:
      timestamp = strftime("%m-%d-%Y %H:%M:%S", time.localtime())
      f.write(timestamp + "\t" + val_str + "\t" + recording_id + "\n")

    return
    
    
    
def CaptureVideo():
  global last_recording
  global recording_id
  
  if((datetime.now() - last_recording) < timedelta(seconds=5)):
    return
    
  recording_id = str(int(time.time()))
  call("sudo raspistill -t 100 -q 75 -w 1024 -h 768 -o /var/www/img/" + recording_id + ".jpg -n", shell=True)
  last_recording = datetime.now()

  filename = strftime("/var/www/%m%d%Y_image.tsv", time.localtime())
  
  if(os.path.exists(filename) == False):
    with open(filename, 'a+') as f:
      f.write("Time\id\n")
      
  with open(filename, 'a+') as f:
    timestamp = strftime("%m-%d-%Y %H:%M:%S", time.localtime())
    f.write(timestamp + "\t" + recording_id + "\n")
  
  return
  
      
if(InitDevice() == False):
    print "unable to open device"
    exit(0)
	  

#datetime.combine(date.today(), last_recording)


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
  
  running_mean = (((running_mean * samples) + val) / (samples + 1))
  if(samples < 100):
    samples += 1
  
  if((datetime.now() - last_recording) > timedelta(seconds=5)):
    recording_id = ""
  
  if((float(val) / running_mean) > 1.25):
    if(val > 700):
      CaptureVideo()

  sys.stdout.write(str(val) + " dB CH: " + str(float(val) / previous_val) + " RM: " + str(float(val) / running_mean) + "\r")
  sys.stdout.flush()
  
  if(.80 < (float(val) / previous_val) < 1.2):
    continue
    
  WriteData(val_str)
  
  previous_val = val;
  
s.close()


