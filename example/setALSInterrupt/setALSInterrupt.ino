/*!
 * @file setALSInterrupt.ino
 * @brief Turn on the ambient light sense interrupt function to obtain the ambient light data within the specified range
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
int state = 0;
int pinInterrupt = 13;
int LEDpin = 12;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(pinInterrupt,INPUT);
  pinMode(LEDpin,OUTPUT);
  digitalWrite(LEDpin,HIGH);
  if(TCS3430.begin()!=true){
    Serial.println("TCS3430 id err");
    return 0;
  }
  TCS3430.enableALSInterrupt(true);
  TCS3430.setIntReadClear(true);
  
  /*
   *                       APERS                              
   * ----------------------------------------------------------
   * | Field Value |            Persistence                   |
   * ----------------------------------------------------------
   * |     0000    |   Every ALS cycle generates an interrupt |
   * ----------------------------------------------------------
   * |     0001    |   Any value outside of threshold range   |
   * ----------------------------------------------------------
   * |     0010    |   2 consecutive values out of range      |
   * ----------------------------------------------------------
   * |     0011    |   3 consecutive values out of range      |
   * ----------------------------------------------------------
   * |     0100    |   5 consecutive values out of range      |
   * ----------------------------------------------------------
   * |     0101    |   10 consecutive values out of range     |
   * ----------------------------------------------------------
   * |     0110    |   15 consecutive values out of range     |
   * ----------------------------------------------------------
   * |     0111    |   20 consecutive values out of range     |
   * ----------------------------------------------------------
   * |     1000    |   25 consecutive values out of range     |
   * ----------------------------------------------------------
   * |     1001    |   30 consecutive values out of range     |
   * ----------------------------------------------------------
   * |     1010    |   35 consecutive values out of range     |
   * ----------------------------------------------------------
   * |     1011    |   40 consecutive values out of range     |
   * ----------------------------------------------------------
   * |     1100    |   45 consecutive values out of range     |
   * ----------------------------------------------------------
   * |     1101    |   50 consecutive values out of range     |
   * ----------------------------------------------------------
   * |     1110    |   55 consecutive values out of range     |
   * ----------------------------------------------------------
   * |     1111    |   60 consecutive values out of range     |
   * ----------------------------------------------------------
   */
  TCS3430.setInterruptPersistence(/*apers=*/0x01);
  // thresholdL\thresholdH:0-65535
  TCS3430.setCH0IntThreshold(/*thresholdL=*/0,/*thresholdH=*/10);
  TCS3430.getDeviceStatus();
}
void loop() {
  // put your main code here, to run repeatedly:
  if(digitalRead(pinInterrupt)==LOW){
    Serial.println("The data obtained exceeds the set threshold");
    TCS3430.getDeviceStatus();
  }
  // put your main code here, to run repeatedly:
  uint16_t XData = TCS3430.getXOrIR2Data();
  uint16_t YData = TCS3430.getYData();
  uint16_t ZData = TCS3430.getZData();
  uint16_t IR1Data = TCS3430.getIR1Data();
  TCS3430.enableIR2(true);
  delay(100);
  uint16_t IR2Data = TCS3430.getXOrIR2Data();
  String str = "X : " + String(XData) + "    Y : " + String(YData) + "    Z : " +  String(ZData) + "    IR1 : "+String(IR1Data) + "    IR2 : "+String(IR2Data);
  Serial.println(str);
  TCS3430.enableIR2(false);
  delay(1000);
}

