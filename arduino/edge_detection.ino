
const byte interruptPin = 2;
volatile unsigned long rising_edges[30];
unsigned long risingTime[30];
volatile int i=0;
int flag;

void setup() {
  Serial.begin(9600);
  pinMode(interruptPin, INPUT);
  attachInterrupt(digitalPinToInterrupt(interruptPin), edgeTime, RISING);
}

void loop() {

   if(i == 30){
     
     for(int index = 0; index < 29; index++){
       risingTime[index] = (rising_edges[index+1] - rising_edges[index]);
       Serial.println(risingTime[index]);
     }
     i = 0;     
  }
  
}

void edgeTime(){
  rising_edges[i] = micros();
  i++;
}
