/*
  Lora Send And Receive
  This sketch demonstrates how to send and receive data with the MKR WAN 1300/1310 LoRa module.
  This example code is in the public domain.
*/

#include <MKRWAN.h>
#include <math.h>

LoRaModem modem;

// Uncomment if using the Murata chip as a module
// LoRaModem modem(Serial1);

#include "arduino_secrets.h"
// Please enter your sensitive data in the Secret tab or arduino_secrets.h
String appEui = SECRET_APP_EUI;
String appKey = SECRET_APP_KEY;

void setup() 
{
    // put your setup code here, to run once:
    Serial.begin(115200);
    while (!Serial);
    // change this to your regional band (eg. US915, AS923, ...)


    while(1)
    {
        GetTemperature();
        delay(500);
    }



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


    //Correction of ADC 
    //analogReadCorrection(260, 2188);


}

void loop() {
  Serial.println();
  Serial.println("Sending a temperature value");

  
    int msg = 55;
    msg++;
    Serial.println();
    Serial.print("Sending: ");
    Serial.print(msg);
    Serial.print(" - ");
    Serial.println();

    int err;
    modem.beginPacket();
    modem.print(msg);
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
}


double GetTemperature(void)
{
    double temperature;
    double voltagemV;
    voltagemV = (double) analogRead(A0);
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
