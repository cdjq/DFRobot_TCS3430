/*!
 * @file getXYZIRData.ino
 * @brief Detection of XYZ tristimulus and infrared data
 * @copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @licence     The MIT License (MIT)
 * @author [yangfeng]<feng.yang@dfrobot.com>
 * @version  V1.0
 * @date  2021-01-26
 * @get from https://www.dfrobot.com
 * @url  https://github.com/DFRobot/DFRobot_TCS3430
 */
#include <DFRobot_TCS3430.h>

DFRobot_TCS3430 TCS3430;
void setup() {
  Serial.begin(115200);

  while(!TCS3430.begin()){
    Serial.println("Please check that the IIC device is properly connected");
    delay(1000);
  }
  // Configure the sensor's ADC integration time, device waiting time, and gain

  //TCS3430.setWaitTimer(true);
  //TCS3430.setWaitLong(false);
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
  //TCS3430.setWaitTime(/*wTime=*/0x00);
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
  //TCS3430.setIntegrationTime(/*aTime=*/0x23);
  /*
   * AGAIN: ALS Gain Control. Sets the gain of the ALS DAC.
   * ----------------------------------------------------------
   * | Field Value |            ALS GAIN VALUE                |
   * ----------------------------------------------------------
   * |     0       |               1X Gain                    |
   * ----------------------------------------------------------
   * |     1       |               4X Gain                    |
   * ----------------------------------------------------------
   * |     2       |               16X Gain                   |
   * ----------------------------------------------------------
   * |     3       |               64X Gain                   |
   * ----------------------------------------------------------
   */
  //TCS3430.setALSGain(/*aGian=*/3);
  //128X high gain
  //TCS3430.setHighGAIN()
}

void loop() {
  uint16_t XData = TCS3430.getXData();
  uint16_t YData = TCS3430.getYData();
  uint16_t ZData = TCS3430.getZData();
  uint16_t IR1Data = TCS3430.getIR1Data();
  uint16_t IR2Data = TCS3430.getIR2Data();
  String str = "X : " + String(XData) + "    Y : " + String(YData) + "    Z : " +  String(ZData) + "    IR1 : "+String(IR1Data) + "    IR2 : "+String(IR2Data);
  Serial.println(str);
  delay(1000);
}
