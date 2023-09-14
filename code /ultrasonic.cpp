//this code is for getting the distance uisng ultrasonic sensors then send it to raspberry pi using serial technique



#include <Servo.h>

const int trig1 = 2;
const int trig2 = 4;
const int trig3 = 7;

const int echo1 = 3;
const int echo2 = 5;
const int echo3 = 8;

#define pwm1 11
#define in1 12
#define in2 13

Servo Servo1;

void setup() {
  pinMode(pwm1, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);

  pinMode(trig1, OUTPUT);
  pinMode(trig2, OUTPUT);
  pinMode(trig3, OUTPUT);

  pinMode(echo1, INPUT);
  pinMode(echo2, INPUT);
  pinMode(echo3, INPUT);

  Servo1.attach(6);  // Attach the servo to pin 6
  Serial.begin(9600);
}

int fdis, rdis, ldis;

void loop() {
  readSensors();  // Read sensor data
  controlServo(); // Control servo based on sensor data
}

void moveForward() {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
}

void turnRight() {
  Servo1.write(180);
}

void turnLeft() {
  Servo1.write(0);
}

void turnBack() {
  Servo1.write(100);
}

int dis(int trig, int echo) {
  long duration;
  int distance;
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  duration = pulseIn(echo, HIGH);
  distance = duration * 0.034 / 2;
  return distance;
}

void readSensors() {
  fdis = dis(trig1, echo1);
  rdis = dis(trig2, echo2);
  ldis = dis(trig3, echo3);
  delay(50);
  Serial.println("FDis:" + String(fdis) + "\tRDis:" + String(rdis) + "\tLDis:" + String(ldis));
}

void controlServo() {
  analogWrite(pwm1, 80);
  moveForward();
  turnBack();
  
  if (fdis < 70) {
    if (ldis < rdis) {
      turnRight();
    }
    if (rdis < ldis) {
      turnLeft();
    }
  }
}
