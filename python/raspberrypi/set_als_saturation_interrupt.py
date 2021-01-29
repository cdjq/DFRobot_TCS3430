""" file set_atime_wtime_gain.py
  # @brief Turn on the ambient light saturation interrupt function
  # @n The experimental phenomena：If the optical data is saturated, the serial port will output a warning
  # @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  # @licence     The MIT License (MIT)
  # @author      [yangfeng]<feng.yang@dfrobot.com> 
  # version  V1.0
  # date  2021-01-26
  # @get from https://www.dfrobot.com
  # @url https://github.com/DFRobot/DFRobot_TCS3430
"""
from DFRobot_TCS3430 import DFRobot_TCS3430
import time
import RPi.GPIO as GPIO

def int_callback(channel):
  print  ('WARNING: channel 0 saturation')
  TCS3430.get_device_status()
  

TCS3430 = DFRobot_TCS3430(bus = 1)
GPIO.setwarnings(False)
# Use GPIO port to monitor sensor interrupt
gpio_int = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(gpio_int, GPIO.IN)
GPIO.add_event_detect(gpio_int, GPIO.FALLING, callback=int_callback) 

#Using GPIO port to control LED of sensor
gpio_led = 11
GPIO.setup(gpio_led, GPIO.OUT)
GPIO.output(gpio_led, GPIO.HIGH)

while(TCS3430.begin() == False ):
  print ('Please check that the IIC device is properly connected.\n')

#Configure the ALS saturation interrupt function of the sensor
TCS3430.set_int_read_clear(mode = True)
'''
  #Maximum ALS Value=  min [CYCLES * 1024, 65535]
  #---------------------------------------------------------------------
  #| aTime | Integration Cycles | Integration Time | Maximum ALS Value |
  #---------------------------------------------------------------------
  #|  0x00 |         1          |       2.78ms     |        1023       |
  #---------------------------------------------------------------------
  #|  0x01 |         2          |       5.56ms     |        2047       |
  #---------------------------------------------------------------------
  #|  ...  |        ...         |       ...        |        ...        |
  #---------------------------------------------------------------------
  #|  0x11 |         18         |       50ms       |        18431      |
  #---------------------------------------------------------------------
  #|  0x40 |         65         |       181ms      |        65535      |
  #---------------------------------------------------------------------
  #|  ...  |        ...         |       ...        |        ...        |
  #---------------------------------------------------------------------
  #|  0xff |        256         |       711ms      |        65535      |
  #---------------------------------------------------------------------
'''
TCS3430.set_integration_time(atime=0x01)
TCS3430.set_als_saturation_interrupt(mode = True)
print ('If the optical data is saturated, an interrupt is triggered and a warning is printed.\r\n')

try:
  while True :
    Z = TCS3430.get_z_data()
    X = TCS3430.get_x_data()
    Y = TCS3430.get_y_data()
    IR1 = TCS3430.get_ir1_data()
    IR2 = TCS3430.get_ir2_data()
    print('X:%d'%X,'Y:%d'%Y,'Z:%d'%Z,'IR1:%d'%IR1,'IR2:%d'%IR2)
    time.sleep(1)
except KeyboardInterrupt:
  GPIO.cleanup() 
