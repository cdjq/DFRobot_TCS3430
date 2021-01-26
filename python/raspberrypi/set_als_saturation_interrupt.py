""" 
  @file set_atime_wtime_gain.py
  @brief Turn on the ambient light saturation interrupt function
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @licence     The MIT License (MIT)
  @author      [yangfeng]<feng.yang@dfrobot.com> 
  version  V1.0
  date  2021-01-26
  @get from https://www.dfrobot.com
  @url https://github.com/DFRobot/DFRobot_SGP40
"""
from DFRobot_TCS3430 import DFRobot_TCS3430
import time
import RPi.GPIO as GPIO

def int_callback(channel):
  print  'channel 0 saturation'
  TCS3430.get_device_status()
  

TCS3430 = DFRobot_TCS3430()

while(TCS3430.begin() == False ):
  print 'equipment id error'

  
gpio_int = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(gpio_int, GPIO.IN)
GPIO.add_event_detect(gpio_int, GPIO.FALLING, callback=int_callback) 

gpio_led = 11;
GPIO.setup(gpio_led, GPIO.OUT)
GPIO.output(gpio_led, GPIO.HIGH)

TCS3430.enable_int_read_clear(mode=True)
"""
Maximum ALS Value=  min [CYCLES * 1024, 65535]
---------------------------------------------------------------------
| aTime | Integration Cycles | Integration Time | Maximum ALS Value |
---------------------------------------------------------------------
|  0x00 |         1          |       2.78ms     |        1023       |
---------------------------------------------------------------------
|  0x01 |         2          |       5.56ms     |        2047       |
---------------------------------------------------------------------
|  ...  |        ...         |       ...        |        ...        |
---------------------------------------------------------------------
|  0x11 |         18         |       50ms       |        18431      |
---------------------------------------------------------------------
|  0x40 |         65         |       181ms      |        65535      |
---------------------------------------------------------------------
|  ...  |        ...         |       ...        |        ...        |
---------------------------------------------------------------------
|  0xff |        256         |       711ms      |        65535      |
---------------------------------------------------------------------
"""
TCS3430.set_integration_time(atime=0x00)

TCS3430.set_als_saturation_interript()
TCS3430.enable_ir2_channel(mode= False)
while True :
  Z = TCS3430.get_ch0_z_data()
  X = TCS3430.get_ch3_x_or_ir2_data()
  Y = TCS3430.get_ch1_y_data()
  TCS3430.enable_ir2_channel(mode= True)
  time.sleep(0.2)
  IR1 = TCS3430.get_ch2_ir1_data()
  IR2 = TCS3430.get_ch3_x_or_ir2_data()
  print 'X:%d'%X,'Y:%d'%Y,'Z:%d'%Z,'IR1:%d'%IR1,'IR2:%d'%IR2
  TCS3430.enable_ir2_channel(mode= False)
  time.sleep(1)
