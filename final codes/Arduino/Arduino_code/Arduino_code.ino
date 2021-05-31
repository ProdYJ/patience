#include <OneWire.h>
#include <Wire.h>
#include <DallasTemperature.h>

//Entrées analogiques
int pinRainOnMe = A2;
int pinLDR_1 = A1;
int pinLDR_2 = A0;
int pinHumidite = A6;

//Entrée digitale
int pin1Wire = 12;

//------------
//1Wire
#define ONE_WIRE_BUS 12
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
int deviceCount = 0; //nombre de sonde, détecté automatiquement dans le void

int tAmbi;
int tInside;
int tBattery;
int tSolarPannel;
int tGround;

//------------
//I2C
#define I2C_SLAVE_ADDRESS 11 // 12 pour l'esclave 2 et ainsi de suite

int pinSDA = 23;
int pinSCL = 24;
int n_I2C = 0;
unsigned long time1;
unsigned long time2;
uint8_t data [16];

//------------
//sunTracking
int seuil_low = 12; //seuil
int seuil_high = 14; //seuil
int night = 400;
int sun1, sun1_correct, sun2; //lecture des LDR
int a = 1, b = 0; //paramètre de calibration
int ecart;
int moyenneLDR = 0;

int sunTracking;
//  =0 : STOP
//  =1 : Montée
//  =2 : Descente

//------------
//Humidity
int humidityLimit = 650;

//------------
//rainSensor
int seuil_rain = 250;
bool rain;
//false = pas de pluie
//true = présence de pluie


void setup() {
  Wire.begin(I2C_SLAVE_ADDRESS);
  Serial.begin(9600);
  Serial.println("-------------------------------------I am Slave1");
  delay(1000);
  Wire.onRequest(requestEvents);
  Wire.onReceive(receiveEvents);

  pinMode(pinRainOnMe, INPUT);
  pinMode(pinLDR_1, INPUT);
  pinMode(pinLDR_2, INPUT);
  pinMode(pin1Wire, INPUT);
  pinMode(pinRainOnMe, INPUT);
  sensors.begin();
  deviceCount = sensors.getDeviceCount();
}

void loop() {
  getTemperature();
  data[0] = humidityDetection();
  sunDetection();
  data[1] = sunTracking;
  data[2] = moyenneLDR;
  rainDetection();
  data[3] = rain;

  data[4] = (uint8_t)5 * tAmbi;
  data[5] = (uint8_t)5 * tInside;
  data[6] = (uint8_t) 1;
  data[7] = (uint8_t) 1;
  data[8] = (uint8_t) 1;
  //data[6] = (uint8_t) tBattery;
  //data[7] = (uint8_t) tSolarPannel;
  //data[8] = (uint8_t) tGround;

  Wire.write((uint8_t *)data, sizeof(data));

  //for (int i = 0; i < 6; i++) {
    //Serial.print(data[i]);
   // Serial.print('\t');
  //
  //Serial.println();
  delay(200);
}

void sunDetection() {

  sun1 = analogRead(pinLDR_1);
  sun2 = analogRead(pinLDR_2);
  Serial.print("sun1 : ");
  Serial.println(sun1);
  Serial.print("sun2 :");
  Serial.println(sun2);

  sun1_correct = a * sun1 + b;

  moyenneLDR = (sun1 + sun1_correct) / 2;

  ecart = abs(sun1_correct - sun2);
  Serial.print("ecart : ");
  Serial.println(ecart);

  if (sun1 > night && sun2 > night) {
    // Serial.println("jour");
    if (ecart > seuil_high) {
      //bouger verin
      if (sun1_correct > sun2) {
        //sens 1
        Serial.println("sun1>sun2");
        sunTracking = 1;
      }
      else {
        //sens 2
         Serial.println("sun1<sun2");
        sunTracking = 2;
      }
    }
    else if (ecart < seuil_low) {
      //Arrêt du verin
      Serial.println("Arrêt du vérin");
      sunTracking = 0;
    }
  }
  else {
    // Serial.println("nuit");
    sunTracking = 3;
  }
}

void rainDetection() {
  //Valeur lue à sec : 1023
  //Valeur lue avec une goutte : au début 80 mais monte à 120 juste après
  int rainReadValue = analogRead(pinRainOnMe);
  if (rainReadValue < seuil_rain) {
    //présence de pluie
    rain = true;
  }
  else {
    //pas de pluie
    rain = false;
  }
}

void getTemperature() {
  sensors.requestTemperatures();
  while (!sensors.isConversionComplete());
  tAmbi = sensors.getTempCByIndex(0);
  tInside = sensors.getTempCByIndex(1);
  //tGround = sensors.getTempCByIndex(2);
  //tSolarPannel = sensors.getTempCByIndex(3);
  // tBattery = sensors.getTempCByIndex(4);

}

int humidityDetection(){
  //retourne 1 si arrosage nécessaire
  //retourne 2 si pas arrosage nécessaire
   int humidityValue = analogRead(pinHumidite);
   //Serial.print("Humidity : "); 
   //Serial.println(humidityValue);
   if(humidityValue > humidityLimit){
     return 1;
   }
   else if(humidityValue<humidityLimit || tAmbi<0){
    return 2;
   }

   return 0;
   
}

void requestEvents(int numByte) {
  Wire.write((uint8_t *) data, sizeof(data));
}

void receiveEvents() {
  int n = Wire.read();
  Wire.write(n);
  //Serial.print("n_I2C:");
  //Serial.println(n_I2C);
}
