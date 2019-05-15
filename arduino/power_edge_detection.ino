
const int SIZE = 496;
const byte interruptPin = 2; //this is the input pin on the arduino
volatile unsigned long rising_edges[SIZE];
unsigned long risingTime[SIZE-1];
volatile int count=0;

/*
 * This program determines the time between rising edges and outputs a list containing those values to the raspberry pi
 * through the serial connection.
 */

void setup() {
  Serial.begin(9600);
  pinMode(interruptPin, INPUT);
  attachInterrupt(digitalPinToInterrupt(interruptPin), edgeTime, RISING);
}

void loop(){

  //Serial.println(count);

   if(count == SIZE){
     
     for(int index = 0; index < SIZE-1; index++){
       risingTime[index] = (rising_edges[index+1]-rising_edges[index]);
       Serial.println(risingTime[index]); 
     }
     count = 0;
     Serial.end();     
  }
  
}

void edgeTime(){
  rising_edges[count] = micros();
  count++;
}
