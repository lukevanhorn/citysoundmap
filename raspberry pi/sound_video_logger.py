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
max_val = 0
min_val = 300


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


def WriteData():
    global recording_id
    global min_val
    global max_val
    
    #max value
    tmp_str = '%d' % max_val
    max_str = tmp_str[:-1] + '.' + tmp_str[-1:]
    
    #min value
    tmp_str = '%d' % min_val
    min_str = tmp_str[:-1] + '.' + tmp_str[-1:]
    
    filename = strftime("/var/www/%m%d%Y.tsv", time.localtime())
    if(os.path.exists(filename) == False):
      with open(filename, 'a+') as f:
        f.write("Time\tdBA\tinfo\n")

    with open(filename, 'a+') as f:
      timestamp = strftime("%m-%d-%Y %H:%M:%S", time.localtime())
      f.write(timestamp + "\t" + max_str + "\t" + recording_id + "\n")

    return
    
    
    
def CaptureVideo():
  global last_recording
  global recording_id
  
  if((datetime.now() - last_recording) < timedelta(seconds=5)):
    return
    
  recording_id = str(int(time.time()))
  call("sudo raspivid -t 5000 -w 640 -h 480 -o /var/www/video/" + recording_id + ".h264; MP4Box -add /var/www/video/" + recording_id + ".h264 /var/www/video/" + recording_id + ".mp4", shell=True)
  last_recording = datetime.now()

  filename = strftime("/var/www/%m%d%Y_video.tsv", time.localtime())
  
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
  # sys.stdout.write('Level: %d ' % (40 + (int(bin(factor), 2) * 20)))

  # Value
  val = ((result[0] & 0x7) << 8) | result[1]
  #tmp_str = '%d' % val
  #val_str = tmp_str[:-1] + '.' + tmp_str[-1:]
  
  if(val > max_val):
    max_val = val
    
  if(val < min_val):
    min_val = val
  
  #running_mean = (((running_mean * samples) + val) / (samples + 1))
  #if(samples < 100):
  #  samples += 1
  
  #writeFlag = False
  
  if((datetime.now() - last_recording) > timedelta(seconds=10)):
    WriteData()
    last_recording = datetime.now()
    min_val = 300
    max_val = 0    
  
  #ratio = (float(val) / previous_val)
  
  #if((ratio < .8) or  (ratio > 1.2)):
  #  writeFlag = True
    
  #if(val > 750):
  #  writeFlag = True  
  
  #if(writeFlag == True):
  #  WriteData()
  
  previous_val = val
  #last_recording = datetime.now()
  
s.close()


