
#define MOTA 5
#define MOTB 6
static char inputString[16];         // a string to hold incoming data
static char direction;               // a string to control which direction we're going in
static char A;
static char B;
int index = 0;
boolean stringComplete = false;  // whether the string is complete

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  
  establishContact();  // send a byte to establish contact until receiver responds 
}

// the loop routine runs over and over again forever:
void loop() {
  // print the string when a newline arrives:
  if (stringComplete) {
    if(inputString=='k') {
      direction = 'k';
    } else if (inByte=='j') {
      direction = 'j'
      while(speed > 0 && speed < 255) {
        analogWrite(MOTB,speed);
        digitalWrite(MOTA,LOW);
        delay(100);
        speed = Serial.read();
      }
      digitalWrite(MOTB,LOW);
    } else if (inByte=='s') {
      digitalWrite(MOTB,LOW);
      digitalWrite(MOTA,LOW);
    } else {
      if(direction == 'j') {
        A = MOTB;
        B = MOTA;
      } else {
        A = MOTA;
        B = MOTB;
      }
      while(inputString > 0 && inputString < 255) {
        analogWrite(A,speed);
        digitalWrite(B,LOW);
        delay(100);
      }
    }
    // clear the string:
    memset ( inputString, 0, 16*sizeof(char) );
    stringComplete = false;
  }
}

void establishContact() {
  while (Serial.available() <= 0) {
    Serial.print('A');   // send a capital A
    delay(300);
  }
}

void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read(); 
    // add it to the inputString:
    inputString[index] = inChar;
    index++;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
      index = 0;
    } 
  }
}