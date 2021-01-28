/*!
 * @file setALSSaturationInterrupt.ino
 * @brief Turn on the ambient light saturation interrupt function
 * @copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @licence     The MIT License (MIT)
 * @author [yangfeng]<feng.yang@dfrobot.com>
 * @version  V1.0
 * @date  2021-01-26
 * @get from https://www.dfrobot.com
 * @url  https://github.com/DFRobot/DFRobot_SGP40
 */
#include <DFRobot_TCS3430.h>


DFRobot_TCS3430 TCS3430;

int LEDpin = 12;
int interruptPin = 2;

volatile int state = 0;

void handleInterrupt(){

  Serial.println("WARNING:Channel 0 saturation （Z Data）");
  state = 1;
}

void setup() {
  Serial.begin(115200);
  
  pinMode(LEDpin,OUTPUT);
  digitalWrite(LEDpin,HIGH);
  pinMode(interruptPin, INPUT_PULLUP);
  
  while(!TCS3430.begin()){
    Serial.println("Please check that the IIC device is properly connected");
    delay(1000);
  }
  
  /*
   * Maximum ALS Value=  min [CYCLES * 1024, 65535]
   * ---------------------------------------------------------------------
   * | aTime | Integration Cycles | Integration Time | Maximum ALS Value |
   * ---------------------------------------------------------------------
   * |  0x00 |         1          |       2.78ms     |        1023       |
   * ---------------------------------------------------------------------
   * |  0x01 |         2          |       5.56ms     |        2047       |
   * ---------------------------------------------------------------------
   * |  ...  |        ...         |       ...        |        ...        |
   * ---------------------------------------------------------------------
   * |  0x11 |         18         |       50ms       |        18431      |
   * ---------------------------------------------------------------------
   * |  0x40 |         65         |       181ms      |        65535      |
   * ---------------------------------------------------------------------
   * |  ...  |        ...         |       ...        |        ...        |
   * ---------------------------------------------------------------------
   * |  0xff |        256         |       711ms      |        65535      |
   * ---------------------------------------------------------------------
   */
  TCS3430.setIntegrationTime(/*aTime=*/0x00);
  TCS3430.setIntReadClear(/*mode*/true);
  //mode = true ： enable ALS Saturation Interrupt
  TCS3430.setALSSaturationInterrupt(/*mode*/true); 

  Serial.println("If the optical data is saturated, an interrupt is triggered and a warning is printed.");
  
  attachInterrupt(digitalPinToInterrupt(interruptPin), handleInterrupt, FALLING);
}

void loop() {
  if (state == 1){
    state =0;
    TCS3430.getDeviceStatus(); 
  }
}