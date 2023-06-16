#include <Servo.h>

Servo pan;
Servo tilt;

String serialStr = "";
int columnIndex = -1;
int pos[2] = {};

int panPos = 90;
int tiltPos = 90;

void setup() {
  pan.attach(3);
  tilt.attach(6);

  Serial.begin(9600);
  Serial.setTimeout(1);
}

void loop() { 
  while (!Serial.available());
  delay(10);//Delay to avoid loop bugs
  serialStr = Serial.readString();
  columnIndex = serialStr.indexOf(':');

  pos[0] = serialStr.substring(0, columnIndex).toInt();
  pos[1] = serialStr.substring(columnIndex+1, serialStr.length()).toInt();

  panPos = map(pos[0], 0, 1000, 0, 180);
  tiltPos = map(pos[1], 0, 1000, 0, 180);

  Serial.println(panPos);
  Serial.println(tiltPos);
  
  pan.write(panPos);
  tilt.write(tiltPos);
}
