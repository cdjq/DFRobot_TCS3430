# DFRobot_TCS3430

The device features advanced digital Ambient Light Sensing (ALS) and CIE 1931 Tristimulus Color Sensing (XYZ). Each of the channels has a filter to control its optical response, which allows the device to accurately measure ambient light and sense color. These measurements are used to calculate chromaticity, illuminance and color temperature, all of which are used to support various potential applications.

## 产品链接（https://www.dfrobot.com/）
    SKU：SEN0403

## Table of Contents

* [Summary](#summary)
* [Installation](#installation)
* [Methods](#methods)
* [Compatibility](#compatibility)
* [History](#history)
* [Credits](#credits)
<snippet>
<content>

## Summary
Detection of XYZ tristimulus and infrared data

## Installation

To use the library, download the library file and place it in a custom directory of the Raspberry Pi

## Methods

```python
  def begin(self):
    """ Set temperature and humidity
    
    :return int equipment condition 
      : 0 succeed
      : 1 failed 
    """

  def set_wait_timer(self,mode=True):
    """ enable wait timer 
    :param mode :bool
      : True enable
      : False disenable
    """
  
  def set_integration_time(self,atime):
    """ Set the internal integration time
    
    :param atime :int the internal integration time
    """

  def set_wait_time(self,wtime):
    """ Set wait time 
    
    :param wtime :wait time
    """

  def set_interrupt_threshold(self,ailt,aiht):
    """ Set the channel 0 interrupt threshold
    
    :param ailt :int the low 16 bit values
    :param ailt :int the high 16 bit values
    """

  def set_interrupt_persistence(self,apers):
    """ Set the channel 0 interrupt Persistence
    
    :param apers :int  Interrupt Persistence
    """

  def set_wait_long_time(self,mode=True):
    """ Set the wait long time
    
    :param mode :bool
      : True enable
      : False disenable
    """
      
  def set_als_gain(self,gain):
    """ Set the ALS gain 
    
    :param gain :int the value of gain
    """

  def get_z_data(self):
    """ get channel 0 value
    
    :return int the z data
    """

  def get_y_data(self):
    """ get channel 1 value
    
    :return int the y data
    """

  def get_ir1_data(self):
    """ get channel 2 value
    
    :return int the IR1 data 
    """

  def get_x_data(self):
    """ get channel 3 value
    
    :return int the X data
    """

  def get_ir2_data(self):
    """ get channel 3 value
    
    :return int the IR2 data
    """

  def set_als_high_gain(self,mode=True):
    """ Set the ALS  128x gain 
    
    :param mode :bool
      : True enable
      : False disenable
    """

  def set_int_read_clear(self,mode=True):
    """If this bit is set, all flag bits in the STATUS register will be reset whenever the STATUS register is read over I2C.
    
    :param mode :bool
      : True enable
      : False disenable
    """

  def set_sleep_after_interrupt(self,mode=True):
    """ Turn on sleep after interruption

    :param mode :bool
      : True enable
      : False disenable
    """
    
  def set_auto_zero_mode(self,mode=0):
    """ set az mode
    :param mode: int 
      :0,Always start at zero when searching the best offset value
      :1,Always start at the previous (offset_c) with the auto-zero mechanism
    """

  def set_auto_zero_nth_iteration(self,iteration_type):
    """ set az nth iteration type(Run autozero automatically every nth ALS iteration)
    :param iteration_type: int 
      :0,never
      :7F,only at first ALS cycle
      :n, every nth time
    """

  def set_als_interrupt(self,mode=True):
    """ enable ambient light sensing interrupt

    :param mode :bool
      : True enable
      : False disenable
    """

  def set_als_saturation_interrupt(self,mode=True):
    """ enable ALS saturation interription
    
    :param mode :bool
      : True enable
      : False disenable
    """

  def get_device_status(self):
    """ Get the status of the device
    
    """

```


## Compatibility

TOOL                | Work Well | Work Wrong | Untested  | Remarks
------------------ | :----------: | :----------: | :---------: | -----
Raspberry Pi |       √      |             |            | 


## History

- data 2021-01-28
- version V1.0


## Credits

·Written by [yangfeng]<feng.yang@dfrobot.com>,2021,(Welcome to our [website](https://www.dfrobot.com/))
