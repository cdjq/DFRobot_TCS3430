""" 
  @file set_atime_wtime_gain.py
  @brief Turn on the ambient light sense interrupt function to obtain the ambient light data within the specified range
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
import pigpio
import RPi.GPIO as GPIO

def int_callback(channel):
  print 'The data obtained exceeds the threshold'
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
while(TCS3430.begin() == False ):
  print 'equipment id error'


TCS3430.enable_wait_timer(mode = True)
TCS3430.set_wait_long_time(mode = False)

"""
By asserting wlong, in register 0x8D the wait time is given in multiples of 33.4ms (12x).
----------------------------------------
| wtime | Wait Cycles | Wait Time      |
----------------------------------------
|  0x00 |      1      | 2.78ms/ 33.4ms |
----------------------------------------
|  0x01 |      2      | 5.56ms/ 66.7ms |
----------------------------------------
|  ...  |     ...     |      ...       |
----------------------------------------
|  0x23 |     36      | 100ms/ 1.20s   |
----------------------------------------
|  ...  |     ...     |       ...      |
----------------------------------------
|  0xff |     256     |  711ms/ 8.53s  |
----------------------------------------
"""
TCS3430.set_wait_time(wtime = 0x00)

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

"""
  AGAIN: ALS Gain Control. Sets the gain of the ALS DAC.
  ----------------------------------------------------------
  | Field Value |            ALS GAIN VALUE                |
  ----------------------------------------------------------
  |     00      |               1X Gain                    |
  ----------------------------------------------------------
  |     01      |               4X Gain                    |
  ----------------------------------------------------------
  |     10      |               16X Gain                   |
  ----------------------------------------------------------
  |     11      |               64X Gain                   |
  ----------------------------------------------------------
"""
TCS3430.set_als_gain(gain=0)
#high_gain =128X Gain
#TCS3430.set_als_high_gain()

"""
  mode
    :0,Always start at zero when searching the best offset value
    :1,Always start at the previous (offset_c) with the auto-zero mechanism
"""
TCS3430.set_auto_zero_mode(mode = 1)

"""
  iteration_type: 
    :0,never
    :7F,only at first ALS cycle
    :n, every nth time
"""
TCS3430.set_auto_zero_nth_iteration(iteration_type = 0x7F)

TCS3430.enable_int_read_clear(True)
TCS3430.set_als_interrupt(True)


"""
                        APERS                              
  ----------------------------------------------------------
  | Field Value |            Persistence                   |
  ----------------------------------------------------------
  |     0000    |   Every ALS cycle generates an interrupt |
  ----------------------------------------------------------
  |     0001    |   Any value outside of threshold range   |
  ----------------------------------------------------------
  |     0010    |   2 consecutive values out of range      |
  ----------------------------------------------------------
  |     0011    |   3 consecutive values out of range      |
  ----------------------------------------------------------
  |     0100    |   5 consecutive values out of range      |
  ----------------------------------------------------------
  |     0101    |   10 consecutive values out of range     |
  ----------------------------------------------------------
  |     0110    |   15 consecutive values out of range     |
  ----------------------------------------------------------
  |     0111    |   20 consecutive values out of range     |
  ----------------------------------------------------------
  |     1000    |   25 consecutive values out of range     |
  ----------------------------------------------------------
  |     1001    |   30 consecutive values out of range     |
  ----------------------------------------------------------
  |     1010    |   35 consecutive values out of range     |
  ----------------------------------------------------------
  |     1011    |   40 consecutive values out of range     |
  ----------------------------------------------------------
  |     1100    |   45 consecutive values out of range     |
  ----------------------------------------------------------
  |     1101    |   50 consecutive values out of range     |
  ----------------------------------------------------------
  |     1110    |   55 consecutive values out of range     |
  ----------------------------------------------------------
  |     1111    |   60 consecutive values out of range     |
  ----------------------------------------------------------
"""
TCS3430.set_interrupt_persistence(apers=0x01)

#ailt\aiht:0-65535
TCS3430.set_interrupt_threshold(ailt=0,aiht=10)

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