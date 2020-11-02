/*
  Lora Send And Receive
  This sketch demonstrates how to send and receive data with the MKR WAN 1300/1310 LoRa module.
  This example code is in the public domain.
*/

#include <MKRWAN.h>
#include <math.h>
#include <stdio.h>

LoRaModem modem;

// Uncomment if using the Murata chip as a module
// LoRaModem modem(Serial1);

#include "arduino_secrets.h"
// Please enter your sensitive data in the Secret tab or arduino_secrets.h
String appEui = SECRET_APP_EUI;
String appKey = SECRET_APP_KEY;

union unpack {
 float payload;
 byte b[4];
};

uint16_t GetTemperature(void);
uint16_t GetLuminosity(void);

void setup() 
{
    // put your setup code here, to run once:
    Serial.begin(115200);
    while (!Serial);
    // change this to your regional band (eg. US915, AS923, ...)

    if (!modem.begin(EU868)) 
    {
      Serial.println("Failed to start module");
      while (1) {}
    };
    Serial.print("Your module version is: ");
    Serial.println(modem.version());
    Serial.print("Your device EUI is: ");
    Serial.println(modem.deviceEUI());
    delay(5000);
    int connected = modem.joinOTAA(appEui, appKey);
    if (!connected) 
    {
      Serial.println("Something went wrong; are you indoor? Move near a window and retry");
      while (1) {}
    }

    // Set poll interval to 60 secs.
    modem.minPollInterval(60);
    // NOTE: independently by this setting the modem will
    // not allow to send more than one message every 2 minutes,
    // this is enforced by firmware and can not be changed.

    //ConfigPins cateur temp // ADC 10 bits sans config particulière
    pinMode(A0, INPUT); 
    pinMode(A1, INPUT); 

    //Correction of ADC 
    //analogReadCorrection(260, 2188);


}

void loop() {
    union unpack temperature;
    byte msg[3];
    uint32_t adcData;

    adcData = 0;
    adcData = GetTemperature();
    adcData = adcData << 10;
    adcData |= GetLuminosity();
    
    msg[0] = adcData >> 16;
    msg[1] = adcData >> 8;
    msg[2] = adcData;
    Serial.print("adcData (32bits) = ");
    Serial.println(adcData);

    Serial.println();
    Serial.print("Sending: ");
    for (uint8_t i =0; i<3 ; i++)
    {
        Serial.print(msg[i]);
    }

    Serial.print(" - ");
    Serial.println();



    int err;
    modem.beginPacket();
    modem.write(msg,3);
    err = modem.endPacket(true);
    if (err > 0) {
      Serial.println("Message sent correctly!");
    } else 
    {
      Serial.println("Error sending message :(");
      Serial.println("(you may send a limited amount of messages per minute, depending on the signal strength");
      Serial.println("it may vary from 1 message every couple of seconds to 1 message every minute)");
    }
    delay(1000);
    if (!modem.available()) 
    {
      Serial.println("No downlink message received at this time.");
      Serial.println("We wait 1 min before sending another message");
      delay(60000);
    }
    delay(30000);
}



uint16_t GetTemperature(void)
{
    uint16_t adcData;
    adcData = analogRead(A0);
    Serial.print("Value of ADC for temp: ");
    Serial.println(adcData);
   return adcData;
}

uint16_t GetLuminosity()//R=3.28 kOhms
{
    uint16_t adcData;
    adcData = analogRead(A1);
    Serial.print("Value of ADC for luminosity: ");
    Serial.println(adcData);
    return adcData;
}


/*
//Rshunt pour mesure de consommation = 10,16 Ohms
float GetTemperature(void)
{
    float temperature;
    float voltagemV;
    voltagemV = (float) analogRead(A0);
    Serial.print("Value of ADC : ");
    Serial.println(voltagemV);
    voltagemV *= 3300/1024.0;
    Serial.print("Value in mV : ");
    Serial.println(voltagemV);
    //Using Equation 1 solved for T at page 10 of LMT84 datasheet
    temperature = ((5.506 - sqrt((-5.506*-5.506)+ (4 * 0.00176 * (870.6-voltagemV)))) / (2 * (-0.00176))) + 30;
    
    Serial.print("Temperature in °C: ");
    Serial.println(temperature);
   return temperature;
}

float GetLuminosity()//R=3.28 kOhms
{
    float voltagemV;
    voltagemV = (float) analogRead(A1);
    voltagemV *= 3300/1024.0;
    return voltagemV;
}
*/