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
#include<DFRobot_TCS3430.h>

DFRobot_TCS3430 TCS3430;

int pinInterrupt = 13;
int LEDpin = 12;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(pinInterrupt,INPUT);
  pinMode(LEDpin,OUTPUT);
  digitalWrite(LEDpin,HIGH);
  while(TCS3430.begin()!=true){
    Serial.println("TCS3430 id err");
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
  TCS3430.enableALSSaturationInterrupt(/*mode*/true); 
}
void loop() {
  // put your main code here, to run repeatedly:
  if(digitalRead(pinInterrupt)==LOW){
    Serial.println("The data obtained exceeds the set threshold");
    TCS3430.getDeviceStatus();
  }
  uint16_t XData = TCS3430.getXOrIR2Data();
  uint16_t YData = TCS3430.getYData();
  uint16_t ZData = TCS3430.getZData();
  uint16_t IR1Data = TCS3430.getIR1Data();
  String str = "X : " + String(XData) + "    Y : " + String(YData) + "    Z : " +  String(ZData) + "    IR1 : "+String(IR1Data);
  Serial.println(str);
  delay(1000);
}
