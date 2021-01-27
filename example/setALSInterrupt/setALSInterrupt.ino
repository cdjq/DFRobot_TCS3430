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
// Configure the sensor's ADC integration time, device waiting time, and gain

  TCS3430.enableWaitTimer(true);
  TCS3430.enableWaitLong(false);
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
  TCS3430.setIntegrationTime(/*aTime=*/0xFF);
  /*
   * By asserting wlong, in register 0x8D the wait time is given in multiples of 33.4ms (12x).
   * ----------------------------------------
   * | wtime | Wait Cycles | Wait Time      |
   * ----------------------------------------
   * |  0x00 |      1      | 2.78ms/ 33.4ms |
   * ----------------------------------------
   * |  0x01 |      2      | 5.56ms/ 66.7ms |
   * ----------------------------------------
   * |  ...  |     ...     |      ...       |
   * ----------------------------------------
   * |  0x23 |     36      | 100ms/ 1.20s   |
   * ----------------------------------------
   * |  ...  |     ...     |       ...      |
   * ----------------------------------------
   * |  0xff |     256     |  711ms/ 8.53s  |
   * ----------------------------------------
   */
  TCS3430.setWaitTime(/*wTime=*/0xFF);
  /*
   * AGAIN: ALS Gain Control. Sets the gain of the ALS DAC.
   * ----------------------------------------------------------
   * | Field Value |            ALS GAIN VALUE                |
   * ----------------------------------------------------------
   * |     00      |               1X Gain                    |
   * ----------------------------------------------------------
   * |     01      |               4X Gain                    |
   * ----------------------------------------------------------
   * |     10      |               16X Gain                   |
   * ----------------------------------------------------------
   * |     11      |               64X Gain                   |
   * ----------------------------------------------------------
   */
  TCS3430.setALSGain(/*aGian=*/1);
  //128X high gain
  //TCS3430.setHighGAIN()
  
// Turn on the ALS interrupt function of the device

  //mode = true : enable ALS Interrupt
  TCS3430.enableALSInterrupt(/*mode*/true);
  //mode = true : turn on "interrupt read clear" function
  TCS3430.setIntReadClear(/*mode*/true);
  //mode = false : turn off "SAL" function
  TCS3430.setSleepAfterInterrupt(/*mode*/false);
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
  TCS3430.setCH0IntThreshold(/*thresholdL=*/0,/*thresholdH=*/500);
  TCS3430.getDeviceStatus();
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
  delay(2000);
}
