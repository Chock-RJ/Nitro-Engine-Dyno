#include <serial-readline.h>
#include <Servo.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 6

// Throttle Control
Servo throttleServo;
int throttlePin = 3;
int throttlePercentage = 0;

//mixture control
Servo mixtureServo;
int mixturePin = 4;
int mixturePercentage = 0;

// Load Control
int loadRequestPin = 5;
int loadRequestPercentage = 0;

// Load Read
int loadActualPin = A5;
int ANALOG_RESOLUTION = 12; // this will need changing to 12 with the new arduni board.
long MAX_ANALOG_UNIT = 4095; // 1023 for 10-bit, 4095 for 12-bit, 16383 for 14-bit.
long MAX_REF_MILLIVOLTAGE = 1100;
long MAX_REF_MICROVOLTAGE = 1100000;

// RPM Read
const int rpmPin = 2;
volatile int rotations;
unsigned long prevMillis;

//temp1 Read
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// Serial Read
void received(char*);
SerialLineReader reader(Serial, received);

void setup() {
  Serial.begin(9600);

  // Temp Sensors
  sensors.begin();
  
  throttleServo.attach(throttlePin);

  mixtureServo.attach(mixturePin);

  //Load Read
  // Sets the maximum analog voltage reference to 1.1 volts,
  // this allows for more precision when measuring millivolts.
  //analogReference(INTERNAL);
  analogReadResolution(ANALOG_RESOLUTION); //un comment this out with the new arduino
  pinMode(loadRequestPin, OUTPUT);

  // RPM Measurement
  pinMode(rpmPin, INPUT);
  attachInterrupt(digitalPinToInterrupt(rpmPin), countRotation, RISING);
  resetCounter();
}

void received(char* line) {
  // Serial.println(line);

if (startsWith(line, "throttle")) {
    // Change "throttle90" to "90"
    char* valueStr = line + strlen("throttle");
    throttlePercentage = atoi(valueStr);
    int throttleVal = map(throttlePercentage, 0, 100, 0, 80);
    throttleServo.write(throttleVal);
    return;
  }

  if (startsWith(line, "mixture")) {
    // Change "mixture90" to "90"
    char* valueStr = line + strlen("mixture");
    mixturePercentage = atoi(valueStr);
    int mixtureVal = map(mixturePercentage, 0, 100, 0, 100);
    mixtureServo.write(mixtureVal);
    return;
  }

  if (startsWith(line, "load")) {
    char* valueStr = line + strlen("load");
    loadRequestPercentage = atoi(valueStr);
    int loadRequestVal = map(loadRequestPercentage, 0, 100, 0, 255);
    analogWrite(loadRequestPin, loadRequestVal);
    return;
  }
}

void loop() {
  reader.poll();

  unsigned long currentMillis = millis();
  unsigned long timeElapsed = currentMillis - prevMillis;

  if (timeElapsed >= 250) {
    noInterrupts();

    // Calculate RPM
    // Take the number of rotations occured in the previous timeElapsed,
    // and then extrapolate that time to a full minute to calculate the RPM.
    long multiplier = 60000 / timeElapsed;
    long rpm = rotations * multiplier;

    // Read and calculate load
    int loadActualVal = analogRead(loadActualPin);
    long loadActualVolts = map(loadActualVal, 0, MAX_ANALOG_UNIT, 0, MAX_REF_MILLIVOLTAGE);

    //Read Temp1
    sensors.requestTemperatures();

    Serial.print(currentMillis);
    Serial.print(",");
    Serial.print(throttlePercentage);
    Serial.print(",");
    Serial.print(loadRequestPercentage);
    Serial.print(",");
    Serial.print(loadActualVolts);
    Serial.print(",");
    Serial.print(rotations);
    Serial.print(",");
    Serial.print(rpm);
    Serial.print(",");
    Serial.print(sensors.getTempCByIndex(0));
    Serial.print(",");
    Serial.print(sensors.getTempCByIndex(1));
    Serial.print(",");
    Serial.print(sensors.getTempCByIndex(2));
    Serial.print("\n");
    
    resetCounter();
    interrupts();
  }
}

void resetCounter() {
  rotations = 0;
  prevMillis = millis();
}

void countRotation() {
  rotations++;
}

bool startsWith(char* str, char* prefix) {
  return strncmp(str, prefix, strlen(prefix)) == 0;
}
