// ASTRA-20/24: banco USB experimental. Sin RF, sensores o actuadores.
// Modelo ilustrativo: apogeo 500 m, descenso 15 m/s hasta 400 m, luego 5 m/s.
#include <Arduino.h>
#include <math.h>
#include "cJSON.h"
#include "esp_system.h"
const char* PROFILE="bench-usb-0.2";
const char* TEAM="1000"; // Ficticio; no es el TEAM_ID asignado.
String bootId,runId="idle",client="",scenario="NOMINAL";
String input,memoId[64],memoInput[64],memoResult[64];
uint32_t highSeq=0,memoIndex=0,tick=0,total=131,nextSample=0;
uint32_t baseSeconds=46800;
float altitudeOffset=12.;bool active=false,discardInput=false;

const char* txt(cJSON* obj,const char* key){cJSON* v=cJSON_GetObjectItemCaseSensitive(obj,key);return cJSON_IsString(v)?v->valuestring:"";}
double num(cJSON* obj,const char* key,double fallback){cJSON* v=cJSON_GetObjectItemCaseSensitive(obj,key);return cJSON_IsNumber(v)?v->valuedouble:fallback;}
cJSON* message(const char* kind){
 cJSON* obj=cJSON_CreateObject();cJSON_AddStringToObject(obj,"v",PROFILE);cJSON_AddStringToObject(obj,"kind",kind);
 cJSON_AddStringToObject(obj,"team",TEAM);cJSON_AddStringToObject(obj,"boot",bootId.c_str());cJSON_AddStringToObject(obj,"run",runId.c_str());return obj;
}
String send(cJSON* obj){
 char* data=cJSON_PrintUnformatted(obj);String result=data?String(data):"";
 if(data){Serial.print("@BENCH ");Serial.print(data);Serial.write('\r');cJSON_free(data);}
 cJSON_Delete(obj);return result;
}
void hello(){cJSON* obj=message("hello");cJSON_AddBoolToObject(obj,"synthetic",true);cJSON_AddStringToObject(obj,"scenario",scenario.c_str());send(obj);}
String response(String id,const char* phase,const char* reason=""){
 cJSON* obj=message("result");cJSON_AddStringToObject(obj,"id",id.c_str());cJSON_AddStringToObject(obj,"phase",phase);
 cJSON_AddBoolToObject(obj,"synthetic",true);if(*reason)cJSON_AddStringToObject(obj,"reason",reason);return send(obj);
}
bool validScenario(String s){return s=="NOMINAL"||s=="PACKET_LOSS"||s=="CORRUPTED_PACKET"||s=="GPS_LOSS"||s=="RESET";}
void process(String line){
 if(!line.startsWith("@BENCH "))return;
 cJSON* obj=cJSON_Parse(line.substring(7).c_str());if(!obj)return;
 if(strcmp(txt(obj,"v"),PROFILE)||strcmp(txt(obj,"team"),TEAM)||strcmp(txt(obj,"kind"),"command")){cJSON_Delete(obj);return;}
 String id=txt(obj,"id"),who=txt(obj,"client"),op=txt(obj,"op");
 double sq=num(obj,"seq",-1);cJSON* args=cJSON_GetObjectItemCaseSensitive(obj,"args");
 if(who.length()<1||who.length()>64||id.length()>96||sq<1||sq>1000000000||sq!=floor(sq)){cJSON_Delete(obj);return;}
 if(id!=who+":"+String((uint32_t)sq)){response(id,"rejected","BAD_ID");cJSON_Delete(obj);return;}
 if(client!=who){client=who;highSeq=0;for(int i=0;i<64;i++){memoId[i]="";memoInput[i]="";memoResult[i]="";}}
 for(int i=0;i<64;i++)if(memoId[i]==id){
  if(memoInput[i]==line){Serial.print("@BENCH ");Serial.print(memoResult[i]);Serial.write('\r');}
  else response(id,"rejected","ID_CONFLICT");cJSON_Delete(obj);return;
 }
 if((uint32_t)sq<=highSeq){response(id,"rejected","ID_EXPIRED");cJSON_Delete(obj);return;}
 highSeq=(uint32_t)sq;String result;
 String sc=txt(args,"scenario");if(sc=="")sc="NOMINAL";
 double requested=num(args,"samples",131);
 if(op=="RUN"&&(!validScenario(sc)||requested<1||requested>100000||requested!=floor(requested)))result=response(id,"rejected","BAD_ARGUMENT");
 else if((op=="CAL_ZERO"||op=="SET_TIME")&&active&&tick>=10)result=response(id,"rejected","NOT_LAUNCH_PAD");
 else if(op=="SET_TIME"&&(num(args,"utc_seconds",-1)<0||num(args,"utc_seconds",-1)>=86400||num(args,"utc_seconds",-1)!=floor(num(args,"utc_seconds",-1))))result=response(id,"rejected","BAD_TIME");
 else if(op!="RUN"&&op!="STOP"&&op!="CAL_ZERO"&&op!="SET_TIME"&&op!="POWER_STATUS")result=response(id,"rejected","UNKNOWN_OPERATION");
 else{
  response(id,"accepted");
  if(op=="RUN"){runId=String(highSeq);scenario=sc;total=(uint32_t)requested;tick=0;active=true;nextSample=millis()+1000;hello();}
  else if(op=="STOP")active=false;
  else if(op=="CAL_ZERO")altitudeOffset=0.;
  else if(op=="SET_TIME")baseSeconds=(uint32_t)num(args,"utc_seconds",46800);
  cJSON* out=message("result");cJSON_AddStringToObject(out,"id",id.c_str());cJSON_AddStringToObject(out,"op",op.c_str());
  cJSON_AddStringToObject(out,"phase","executed");cJSON_AddBoolToObject(out,"synthetic",true);
  if(op=="POWER_STATUS"){cJSON_AddNumberToObject(out,"voltage",fmax(3.6,4.1-.5*tick/7200.));cJSON_AddNumberToObject(out,"solar_voltage",2.5);}
  if(op=="CAL_ZERO")cJSON_AddNumberToObject(out,"altitude_zero",0.);
  if(op=="SET_TIME")cJSON_AddNumberToObject(out,"utc_seconds",baseSeconds);
  result=send(out);
 }
 unsigned index=memoIndex++%64;memoId[index]=id;memoInput[index]=line;memoResult[index]=result;cJSON_Delete(obj);
}
String clockText(uint32_t t){char value[12];t=(baseSeconds+t)%86400;snprintf(value,sizeof(value),"%02lu:%02lu:%02lu",(unsigned long)(t/3600),(unsigned long)((t/60)%60),(unsigned long)(t%60));return String(value);}
float height(uint32_t t){
 if(t<10)return 0.;if(t<30){float u=t-10;return 50*u-1.25*u*u;}
 float u=t-30;if(u<100./15)return 500-15*u;return fmax(0.,400-5*(u-100./15));
}
void emitSample(uint32_t t){
 bool omitted=(scenario=="PACKET_LOSS"&&t%10==5)||(scenario=="RESET"&&t>=60&&t<63);
 bool corrupt=scenario=="CORRUPTED_PACKET"&&t%13==6;
 cJSON* oracle=message("oracle");cJSON_AddNumberToObject(oracle,"count",t+1);
 cJSON_AddStringToObject(oracle,"outcome",omitted?"omitted":(corrupt?"corrupted":"emitted"));cJSON_AddStringToObject(oracle,"scenario",scenario.c_str());send(oracle);
 if(omitted)return;
 float h=height(t);const char* state;
 if(t<10)state="LAUNCH_PAD";else if(t<30)state="ASCENT";else if(t==30)state="APOGEE";
 else if(t-30<100./15)state="DESCENT";else if(h<=0)state="LANDED";else if(t==37)state="PROBE_RELEASE";else state="PAYLOAD_RELEASE";
 bool lost=scenario=="GPS_LOSS"&&t>=50&&t<65;uint32_t gt=lost?49:t;
 String v[22]={String(TEAM),clockText(t),String(t+1),"S",state,
 String(h+altitudeOffset,1),String(23-.0065*h,1),String(101.325*pow(1-2.25577e-5*h,5.25588),1),
 String(fmax(3.6,4.1-.5*t/7200.),2),String(t==37?.28:.18,2),
 String(2*sin(t/5.),2),String(cos(t/6.),2),String(sin(t/7.),2),"0.00","0.00",String((t<10||h<=0)?9.81:9.81+.2*sin(t),2),
 clockText(gt),String(height(gt)+30,1),String(-34.6+gt*.000001,4),String(-58.4+gt*.000001,4),String(lost?0:9),"NONE"};
 if(corrupt)v[7]="BAD";
 for(int i=0;i<22;i++){if(i)Serial.write(',');Serial.print(v[i]);}Serial.write('\r');
}
void setup(){
 Serial.begin(115200);char id[20];snprintf(id,sizeof(id),"%08lx%08lx",(unsigned long)esp_random(),(unsigned long)esp_random());bootId=id;
 delay(100);Serial.write('\r');hello();
}
void loop(){
 while(Serial.available()){
  char ch=Serial.read();if(ch=='\r'){
   if(!discardInput&&input.length())process(input);input="";discardInput=false;
  }else if(ch!='\n'&&!discardInput){input+=ch;if(input.length()>1024){input="";discardInput=true;}}
 }
 if(active&&(int32_t)(millis()-nextSample)>=0){emitSample(tick++);nextSample=millis()+1000;
  if(tick>=total){active=false;cJSON* obj=message("done");cJSON_AddNumberToObject(obj,"samples",total);cJSON_AddStringToObject(obj,"scenario",scenario.c_str());send(obj);}
 }
 delay(1);
}
