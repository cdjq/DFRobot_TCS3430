""" 
  @file set_atime_wtime_gain.py
  @brief Detection of XYZ tristimulus and infrared data
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

TCS3430 = DFRobot_TCS3430()

GPIO.setmode(GPIO.BOARD)
gpio_led = 11;
GPIO.setup(gpio_led, GPIO.OUT)
GPIO.output(gpio_led, GPIO.HIGH)

while(TCS3430.begin() == False ):
  print 'equipment id error'

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