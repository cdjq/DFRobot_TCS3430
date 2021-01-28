""" file DFRobot_TCS3430.py
  # DFRobot_TCS3430 Class infrastructure, implementation of underlying methods
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @licence     The MIT License (MIT)
  @author      [yangfeng]<feng.yang@dfrobot.com> 
  @version  V1.0
  @date  2021-01-26
  @get from https://www.dfrobot.com
  @url https://github.com/DFRobot/DFRobot_TCS3430
"""
import smbus
import time

class DFRobot_TCS3430:
  DFRobot_TCS3430_IIC_ADDR           = 0x39
  
  TCS3430_REG_ENABLE_ADDR            = 0x80
  TCS3430_REG_ATIME_ADDR             = 0x81
  TCS3430_REG_WTIME_ADDR             = 0x83
  TCS3430_REG_AILTL_ADDR             = 0x84
  TCS3430_REG_AILTH_ADDR             = 0x85
  TCS3430_REG_AIHTL_ADDR             = 0x86
  TCS3430_REG_AIHTH_ADDR             = 0x87
  TCS3430_REG_PERS_ADDR              = 0x8C
  TCS3430_REG_CFG0_ADDR              = 0x8D
  TCS3430_REG_CFG1_ADDR              = 0x90
  TCS3430_REG_REVID_ADDR             = 0x91
  TCS3430_REG_ID_ADDR                = 0x92
  TCS3430_REG_STATUS_ADDR            = 0x93
  TCS3430_REG_CH0DATAL_ADDR          = 0x94
  TCS3430_REG_CH0DATAH_ADDR          = 0x95
  TCS3430_REG_CH1DATAL_ADDR          = 0x96
  TCS3430_REG_CH1DATAH_ADDR          = 0x97
  TCS3430_REG_CH2DATAL_ADDR          = 0x98
  TCS3430_REG_CH2DATAH_ADDR          = 0x99
  TCS3430_REG_CH3DATAL_ADDR          = 0x9A
  TCS3430_REG_CH3DATAH_ADDR          = 0x9B
  TCS3430_REG_CFG2_ADDR              = 0x9F
  TCS3430_REG_CFG3_ADDR              = 0xAB
  TCS3430_REG_AZCONFIG_ADDR          = 0xD6
  TCS3430_REG_INTENAB_ADDR           = 0xDD
  
  ENABLEREG_POWER_ON                 = 0x01
  ENABLEREG_POWER_OFF                = 0xFE
  ENABLEREG_ALS_EN                   = 0x02
  ENABLEREG_ALS_DISEN                = 0xFD
  ENABLEREG_WAIT_EN                  = 0x08
  ENABLEREG_WAIT_DISEN               = 0xF7
  
  CONFIG_NO_WLONG                    = 0x80
  CONFIG_WLONG                       = 0x84
  
  CFG1_IR2_EN                        = 0x08
  CFG1_IR2_DISEN                     = 0xF7
  
  CFG2_HIGH_GAIN_EN                  = 0x14
  CFG2_HIGH_GAIN_DISEN               = 0x04
  
  CFG3_INT_READ_CLEAR_EN             = 0x80
  CFG3_INT_READ_CLEAR_DISEN          = 0x10
  CFG3_SAI_EN                        = 0x10
  CFG3_SAI_DISEN                     = 0x80

  AZ_MODE_0                          = 0x7F
  AZ_MODE_1                          = 0x80
  
  ENABLEREG_ALS_INT_EN               = 0x10
  ENABLEREG_ALS_INT_DISEN            = 0x80
  ALS_SATURATION_INTERRUPT_EN        = 0x80
  ALS_SATURATION_INTERRUPT_DISEN     = 0x10
  
  TCS3430_ID                         = 0xDC
  TCS3430_REVISION_ID                = 0x41
  def __init__(self,bus = 1):
    """ Module init
    
    :param bus:int Set to IICBus
    """
    self.__i2cbus = smbus.SMBus(bus)
    self.__i2c_addr = self.DFRobot_TCS3430_IIC_ADDR
    self.__i2c_addr = 0x39
    self.__wlong = 0
    self.__atime = 0
    self.__wtime = 0

  def begin(self):
    """ Set temperature and humidity
    
    :return int equipment condition 
      : 0 succeed
      : 1 failed 
    """
    self.__soft_reset()
    self.__set_power_als_on()
    device_id = self.__get_device_id()
    revision_id =self.__get_revision_id()
    if device_id != self.TCS3430_ID and revision_id != self.TCS3430_REVISION_ID :
      self.__set_device_adc(False)
      self.__set_device_power(False)
      return False
    return True 

  def set_wait_timer(self,mode=True):
    """ enable wait timer 
    :param mode :bool
      : True enable
      : False disenable
    """
    if mode==True:
      self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_ENABLE_ADDR, self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_ENABLE_ADDR)|self.ENABLEREG_WAIT_EN)
    if mode==False:
      self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_ENABLE_ADDR, self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_ENABLE_ADDR)&self.ENABLEREG_WAIT_DISEN)
  
  def set_integration_time(self,atime):
    """ Set the internal integration time
    
    :param atime :int the internal integration time
    """
    atime = atime & 0xFF
    self.__atime = atime
    self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_ATIME_ADDR, atime)

  def set_wait_time(self,wtime):
    """ Set wait time 
    
    :param wtime :wait time
    """
    wtime = wtime & 0xFF
    self.__wtime = wtime
    self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_WTIME_ADDR, wtime)

  def set_interrupt_threshold(self,ailt,aiht):
    """ Set the channel 0 interrupt threshold
    
    :param ailt :int the low 16 bit values
    :param ailt :int the high 16 bit values
    """
    ailtl = ailt & 0xFF
    ailth = (ailt>>8) & 0xFF
    aihtl = aiht & 0xFF
    aihth = (aiht>>8) & 0xFF
    self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_AILTL_ADDR, ailtl)
    self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_AILTH_ADDR, ailth)
    self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_AIHTL_ADDR, aihtl)
    self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_AIHTH_ADDR, aihth)

  def set_interrupt_persistence(self,apers):
    """ Set the channel 0 interrupt Persistence
    
    :param apers :int  Interrupt Persistence
    """
    apers = apers & 0xFF
    self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_PERS_ADDR, apers)



  def set_wait_long_time(self,mode=True):
    """ Set the wait long time
    
    :param mode :bool
      : True enable
      : False disenable
    """
    if mode == True:
      self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_CFG0_ADDR, self.CONFIG_WLONG)
      self.__wlong = 1
    if mode == False:
      self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_CFG0_ADDR, self.CONFIG_NO_WLONG)
      self.__wlong = 0
      
  def set_als_gain(self,gain):
    """ Set the ALS gain 
    
    :param gain :int the value of gain
    """
    gain = gain & 0xFF
    self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_CFG1_ADDR, self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_CFG1_ADDR)|gain)

  def get_z_data(self):
    """ get channel 0 value
    
    :return int the z data
    """
    vlaue = self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_CH0DATAL_ADDR)
    data = vlaue | (self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_CH0DATAH_ADDR)<<8)
    return data 

  def get_y_data(self):
    """ get channel 1 value
    
    :return int the y data
    """
    value = self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_CH1DATAL_ADDR)
    value = value | (self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_CH1DATAH_ADDR)<<8)
    return value 

  def get_ir1_data(self):
    """ get channel 2 value
    
    :return int the IR1 data 
    """
    value = self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_CH2DATAL_ADDR)
    value = value | (self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_CH2DATAH_ADDR)<<8)
    return value 

  def get_x_data(self):
    """ get channel 3 value
    
    :return int the X data
    """
    value = self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_CH3DATAL_ADDR)
    value = value | (self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_CH3DATAH_ADDR)<<8)
    return value 

  def get_ir2_data(self):
    """ get channel 3 value
    
    :return int the IR2 data
    """
    self.__set_ir2_channel(True)
    if (self.__wlong):
      delaytime = ((self.__atime+1)*2.78 + (self.__wtime+1)*33.4)/1000
    else:
      delaytime =((self.__atime+1)*2.78 + (self.__wtime+1)*2.78)/1000
    time.sleep(delaytime)
    value = self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_CH3DATAL_ADDR)
    value = value | (self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_CH3DATAH_ADDR)<<8)
    self.__set_ir2_channel(False)
    time.sleep(delaytime)
    return value 

  def set_als_high_gain(self,mode=True):
    """ Set the ALS  128x gain 
    
    :param mode :bool
      : True enable
      : False disenable
    """
    if mode == True:
      self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_CFG2_ADDR, self.CFG2_HIGH_GAIN_EN)
    if mode == False:
      self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_CFG2_ADDR, self.CFG2_HIGH_GAIN_DISEN)

  def set_int_read_clear(self,mode=True):
    """If this bit is set, all flag bits in the STATUS register will be reset whenever the STATUS register is read over I2C.
    
    :param mode :bool
      : True enable
      : False disenable
    """
    if mode == True:
      self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_CFG3_ADDR, self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_CFG3_ADDR)|self.CFG3_INT_READ_CLEAR_EN)
    if mode == False:
      self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_CFG3_ADDR, self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_CFG3_ADDR)|self.CFG3_INT_READ_CLEAR_DISEN)

  def set_sleep_after_interrupt(self,mode=True):
    """ Turn on sleep after interruption

    :param mode :bool
      : True enable
      : False disenable
    """
    if mode == True:
      self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_CFG3_ADDR, self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_CFG3_ADDR)|self.CFG3_SAI_EN)
    if mode == False:
      self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_CFG3_ADDR, self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_CFG3_ADDR)|self.CFG3_SAI_DISEN)

  def set_auto_zero_mode(self,mode=0):
    """ set az mode
    :param mode: int 
      :0,Always start at zero when searching the best offset value
      :1,Always start at the previous (offset_c) with the auto-zero mechanism
    """
    if(mode==1):
      self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_AZCONFIG_ADDR, self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_AZCONFIG_ADDR)|self.AZ_MODE_1)
    if(mode==0):
      self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_AZCONFIG_ADDR, self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_AZCONFIG_ADDR)&self.AZ_MODE_0)

  def set_auto_zero_nth_iteration(self,iteration_type):
    """ set az nth iteration type(Run autozero automatically every nth ALS iteration)
    :param iteration_type: int 
      :0,never
      :7F,only at first ALS cycle
      :n, every nth time
    """
    iteration_type = iteration_type & 0x7F
    self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_AZCONFIG_ADDR, self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_AZCONFIG_ADDR)|iteration_type)

  def set_als_interrupt(self,mode=True):
    """ enable ambient light sensing interrupt

    :param mode :bool
      : True enable
      : False disenable
    """
    if(mode==True):
      self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_INTENAB_ADDR, self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_INTENAB_ADDR)|self.ENABLEREG_ALS_INT_EN)
    if(mode==False):
      self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_INTENAB_ADDR, self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_ENABLE_ADDR)&self.ENABLEREG_ALS_INT_DISEN)

  def set_als_saturation_interrupt(self,mode=True):
    """ enable ALS saturation interription
    
    :param mode :bool
      : True enable
      : False disenable
    """
    if(mode==True):
      self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_INTENAB_ADDR, self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_INTENAB_ADDR)|self.ALS_SATURATION_INTERRUPT_EN)
    if(mode==False):
      self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_INTENAB_ADDR, self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_INTENAB_ADDR)&self.ALS_SATURATION_INTERRUPT_DISEN)

  def get_device_status(self):
    """ Get the status of the device
    
    """
    self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_STATUS_ADDR)

  def __set_ir2_channel(self,mode=True):
    """ Access to IR channel; allows mapping of IR channel on channel 3.
    
    :param mode :bool
      : True enable
      : False disenable
    """
    if mode == True:
      self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_CFG1_ADDR, self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_CFG1_ADDR)|self.CFG1_IR2_EN)
    if mode == False:
      self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_CFG1_ADDR, self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_CFG1_ADDR)&self.CFG1_IR2_DISEN)
      
  def __set_power_als_on(self):
    """ Activating the internal oscillator to permit the timers and ADC channels to operate ,and activing the ALS function
    
    """
    self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_ENABLE_ADDR, self.ENABLEREG_ALS_EN|self.ENABLEREG_POWER_ON)

  def __set_device_power(self,mode=True):
    """ Activating the internal oscillator to permit the timers and ADC channels to operate
    
    :param mode :bool
      : True enable
      : False disenable
    """
    if(mode==True):
      self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_ENABLE_ADDR, self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_ENABLE_ADDR)|self.ENABLEREG_POWER_ON)
    if(mode==False):
      self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_ENABLE_ADDR, self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_ENABLE_ADDR)&self.ENABLEREG_POWER_OFF)

  def __set_device_adc(self,mode=True):
    """ Activating the four-channel ADC
    
    :param mode :bool
      : True enable
      : False disenable
    """
    if(mode==True):
      self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_ENABLE_ADDR, self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_ENABLE_ADDR)|self.ENABLEREG_ALS_EN)
    if(mode==False):
      self.__i2cbus.write_byte_data(self.__i2c_addr,self.TCS3430_REG_ENABLE_ADDR, self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_ENABLE_ADDR)&self.ENABLEREG_ALS_DISEN)

  def __get_revision_id(self):
    """ get the revision id
    
    :return int the revision id
    """
    return self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_REVID_ADDR)

  def __get_device_id(self):
    """ get the device id
    
    :return int the device id
    """
    a = self.__i2cbus.read_byte_data(self.__i2c_addr,self.TCS3430_REG_ID_ADDR)
    return a

  def __soft_reset(self):
    """ Initializes all registers of the device

    """
    self.set_wait_timer(False)
    self.set_integration_time(False)
    self.set_wait_time(0)
    self.set_wait_long_time(False)
    self.set_als_gain(0)
    self.set_als_high_gain(False)
    self.set_int_read_clear(False)
    self.set_sleep_after_interrupt(False)
    self.set_auto_zero_mode(0)
    self.set_auto_zero_nth_iteration(0x7F)
    self.set_als_saturation_interrupt(False)
    self.set_als_interrupt(False)

    