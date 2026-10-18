// Diagnostic: prints raw A0 statistics once per second (IR LED on D9 kept ON).
void setup(){pinMode(9,OUTPUT);digitalWrite(9,HIGH);Serial.begin(115200);delay(1500);Serial.println(F("DIAG mean_V min max pp samples"));}
void loop(){
  unsigned long t=millis();long sum=0;int mn=1023,mx=0;int n=0;
  while(millis()-t<1000){int v=analogRead(A0);sum+=v;if(v<mn)mn=v;if(v>mx)mx=v;n++;delay(2);}
  Serial.print(F("DIAG "));Serial.print(sum/(float)n*5.0/1023.0,2);Serial.print(' ');Serial.print(mn);Serial.print(' ');Serial.print(mx);Serial.print(' ');Serial.print(mx-mn);Serial.print(' ');Serial.println(n);
}
