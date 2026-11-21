// ASTRA USB-only bench simulator. No SX1276, no RF profile, no actuators.
// Board model TBD. Arduino ESP32 core required; verify board before flashing.
// TEAM_ID 1000 is CONAE's imaginary example, NOT an assigned ASTRA ID.
#include <Arduino.h>
#include <math.h>
const char* TEAM_ID = "1000";
enum Scenario { NOMINAL, PACKET_LOSS, CORRUPTED_PACKET, GPS_LOSS, RESET };
const Scenario SCENARIO = NOMINAL; // Change only this selector for bench faults.
uint32_t tick = 0;
uint32_t nextSample;

String clockText(uint32_t t) {
  char value[12];
  snprintf(value, sizeof(value), "%02lu:%02lu:%02lu",
    (unsigned long)(13+t/3600), (unsigned long)((t/60)%60), (unsigned long)(t%60));
  return String(value);
}
void emitSample(uint32_t t) {
  float h;
  const char* state;
  if (t<10) { h=0; state="LAUNCH_PAD"; }
  else if (t<30) { float u=t-10; h=50*u-1.25*u*u; state="ASCENT"; }
  else if (t==30) { h=500; state="APOGEE"; }
  else if (t<40) { float u=t-30; h=500-u*u; state="DESCENT"; }
  else if (t==40) { h=400; state="PROBE_RELEASE"; }
  else if (t<120) { h=400-5*(t-40); state="PAYLOAD_RELEASE"; }
  else { h=0; state="LANDED"; }
  // Skips represent emitted-but-not-delivered observations for PC gap tests.
  // RESET is logical only, NOT ESP.restart(): state remains in RAM.
  if (SCENARIO==RESET && t>=60 && t<63) return;
  if (SCENARIO==PACKET_LOSS && t%10==5) return;
  bool gpsLost=SCENARIO==GPS_LOSS && t>=50 && t<65;
  uint32_t gt=gpsLost?49:t;
  float gh=gpsLost?385:h+30;
  String values[22]={
    String(TEAM_ID),clockText(t),String(t+1),"S",String(state),
    String(h,1),String(23-.0065*h,1),String(101.325*pow(1-2.25577e-5*h,5.25588),1),
    String(4.1-.0008*t,1),String(.18+(t==40?.1:0),2),
    String(2*sin(t/5.0),2),String(cos(t/6.0),2),String(sin(t/7.0),2),
    "0.00","0.00",String(t<10 || t>=120?9.81:9.81+.2*sin(t),2),
    clockText(gt),String(gh,1),String(-34.6+gt*.000001,4),
    String(-58.4+gt*.000001,4),String(gpsLost?0:9),"NONE"
  };
  if (SCENARIO==CORRUPTED_PACKET && t%13==6) values[7]="BAD";
  for (int i=0;i<22;i++) {
    if (i) Serial.write(',');
    Serial.print(values[i]);
  }
  Serial.write('\r'); // Official CR, never println/CRLF.
}
void setup() {
  Serial.begin(115200); // Local USB bench setting, NOT an RF parameter.
  nextSample=millis()+1000;
}
void loop() {
  if (tick>130) { delay(10); return; }
  uint32_t now=millis();
  if ((int32_t)(now-nextSample)>=0) {
    emitSample(tick++);
    nextSample=now+1000; // No catch-up bursts if execution is delayed.
  }
  delay(1);
}
