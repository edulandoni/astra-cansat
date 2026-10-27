// ASTRA-39: candidato de mantenimiento Wi-Fi, separado del firmware probado.
// No implemento interfaz de vuelo. Radio apagada al arrancar; activacion local explicita.
#include <Arduino.h>
#include "esp_camera.h"
#include "esp_log.h"
#include "esp_timer.h"
#include "FS.h"
#include "SD_MMC.h"

static bool cameraReady=false;
static esp_err_t cameraError=ESP_FAIL;
static char bootId[17];
static char deviceId[17];
static char input[81];
static size_t used=0;
static bool overflow=false;

uint32_t crc32data(const uint8_t *data,size_t n,uint32_t crc=0xffffffffU) {
  while(n--) {crc^=*data++;for(int j=0;j<8;j++)crc=(crc>>1)^((crc&1)?0xedb88320U:0);}
  return crc;
}
void error(const char *id,const char *reason) {
  Serial.printf("@CAM {\"v\":1,\"event\":\"error\",\"id\":\"%s\",\"boot\":\"%s\",\"reason\":\"%s\"}\n",id,bootId,reason);
}
void info(const char *id) {
  sensor_t *s=cameraReady?esp_camera_sensor_get():nullptr;
  Serial.printf("@CAM {\"v\":1,\"event\":\"info\",\"id\":\"%s\",\"boot\":\"%s\",\"device\":\"%s\",\"profile\":\"camera-usb-0.1\",\"commands\":[\"INFO\",\"INIT\",\"PHOTO\",\"SAVE\",\"CLIP\",\"WIFI_ON\",\"WIFI_OFF\"],\"camera_ready\":%s,\"camera_init_error\":\"%s\",\"sensor_pid\":%u,\"psram_bytes\":%u,\"flash_bytes\":%u,\"wifi_started_at_boot\":false,\"sd_checked\":false}\n",
    id,bootId,deviceId,cameraReady?"true":"false",esp_err_to_name(cameraError),s?s->id.PID:0,ESP.getPsramSize(),ESP.getFlashChipSize());
}
void initializeCamera();
void photo(const char *id,bool save) {
  if(!cameraReady){error(id,"CAMERA_INIT_FAILED");return;}
  // Habilito diagnóstico sólo durante adquisición, nunca dentro del JPEG binario.
  struct CaptureLog {
    CaptureLog(){esp_log_level_set("*",ESP_LOG_WARN);}
    ~CaptureLog(){esp_log_level_set("*",ESP_LOG_NONE);}
  } captureLog;
  int64_t requestUs=esp_timer_get_time();
  // Descarto cuadros en espera; no uso una foto almacenada como chequeo nuevo.
  for(int i=0;i<2;i++){
    Serial.printf("#CAM warmup %d\n",i+1);
    camera_fb_t *old=esp_camera_fb_get();
    if(!old){error(id,i==0?"WARMUP_1_FAILED":"WARMUP_2_FAILED");return;}
    esp_camera_fb_return(old);delay(80);
  }
  Serial.println("#CAM requested frame");
  camera_fb_t *fb=esp_camera_fb_get();
  if(!fb){error(id,"REQUESTED_FRAME_FAILED");return;}
  esp_log_level_set("*",ESP_LOG_NONE);
  int64_t captureUs=(int64_t)fb->timestamp.tv_sec*1000000+fb->timestamp.tv_usec;
  if(captureUs<requestUs){esp_camera_fb_return(fb);error(id,"STALE_FRAME");return;}
  if(fb->format!=PIXFORMAT_JPEG || fb->len<4 || fb->len>512*1024 || fb->buf[0]!=0xff || fb->buf[1]!=0xd8 || fb->buf[fb->len-2]!=0xff || fb->buf[fb->len-1]!=0xd9){
    esp_camera_fb_return(fb);error(id,"INVALID_JPEG");return;
  }
  uint32_t crc=crc32data(fb->buf,fb->len)^0xffffffffU;
  bool saved=false;const char *sdStatus="NOT_REQUESTED";char path[80]="";
  if(save){
    // Nunca formateo ni borro. Monto en un bit para no usar GPIO4 del flash LED.
    esp_log_level_set("*",ESP_LOG_WARN);
    bool mounted=SD_MMC.begin("/sdcard",true,false);
    esp_log_level_set("*",ESP_LOG_NONE);
    if(!mounted){sdStatus="MOUNT_FAILED";}
    else {
      snprintf(path,sizeof(path),"/ASTRA_CHECK_%s_%s.jpg",bootId,id);
      if(SD_MMC.exists(path)){sdStatus="EXISTS_REFUSED";}
      else {
        File f=SD_MMC.open(path,FILE_WRITE);
        if(!f){sdStatus="OPEN_FAILED";}
        else {
          size_t written=f.write(fb->buf,fb->len);f.flush();f.close();
          if(written!=fb->len){sdStatus="SHORT_WRITE";}
          else {
            File check=SD_MMC.open(path,FILE_READ);
            if(!check){sdStatus="READ_FAILED";}
            else {
              uint32_t readCrc=0xffffffffU;size_t total=0;uint8_t block[512];
              while(check.available()){
                size_t got=check.read(block,sizeof(block));if(!got)break;
                readCrc=crc32data(block,got,readCrc);total+=got;
              }
              check.close();saved=total==fb->len && (readCrc^0xffffffffU)==crc;
              sdStatus=saved?"READBACK_OK":"READBACK_MISMATCH";
            }
          }
        }
      }
      SD_MMC.end();
    }
  }
  Serial.printf("@CAM {\"v\":1,\"event\":\"frame\",\"id\":\"%s\",\"boot\":\"%s\",\"device\":\"%s\",\"request_us\":%lld,\"capture_us\":%lld,\"length\":%u,\"crc32\":\"%08lx\",\"width\":%u,\"height\":%u,\"saved\":%s,\"sd_status\":\"%s\",\"path\":\"%s\"}\n",
    id,bootId,deviceId,(long long)requestUs,(long long)captureUs,(unsigned)fb->len,(unsigned long)crc,(unsigned)fb->width,(unsigned)fb->height,saved?"true":"false",sdStatus,path);
  Serial.write(fb->buf,fb->len);Serial.flush();
  Serial.printf("\n@CAM {\"v\":1,\"event\":\"end\",\"id\":\"%s\",\"boot\":\"%s\"}\n",id,bootId);
  esp_camera_fb_return(fb);
}
#include "sequence_capture.h"
#include "preview_wifi.h"

void command(char *line) {
  if(previewCommand(line))return;
  char *space=strchr(line,' ');if(!space){error("","BAD_COMMAND");return;}
  *space=0;char *id=space+1;
  if(strlen(id)!=16){error("","BAD_ID");return;}
  for(int i=0;i<16;i++)if(!isxdigit((unsigned char)id[i])){error("","BAD_ID");return;}
  if(!strcmp(line,"INFO"))info(id);
  else if(!strcmp(line,"INIT")){initializeCamera();info(id);}
  else if(!strcmp(line,"PHOTO"))photo(id,false);
  else if(!strcmp(line,"SAVE"))photo(id,true);
  else if(!strcmp(line,"CLIP"))sequenceClip(id);
  else error(id,"UNKNOWN_COMMAND");
}
void setup() {
  Serial.begin(115200);Serial.setDebugOutput(false);esp_log_level_set("*",ESP_LOG_NONE);
  snprintf(bootId,sizeof(bootId),"%08lx%08lx",(unsigned long)esp_random(),(unsigned long)esp_random());
  snprintf(deviceId,sizeof(deviceId),"%016llx",(unsigned long long)ESP.getEfuseMac());
  initializeCamera();delay(200);info("");
}
void initializeCamera() {
  if(cameraReady)esp_camera_deinit();
  cameraReady=false;
  // Perfil candidato AI-Thinker de Espressif: verifico la placa antes de cargar.
  pinMode(4,OUTPUT);digitalWrite(4,LOW);
  camera_config_t c={};c.ledc_channel=LEDC_CHANNEL_0;c.ledc_timer=LEDC_TIMER_0;
  c.pin_d0=5;c.pin_d1=18;c.pin_d2=19;c.pin_d3=21;c.pin_d4=36;c.pin_d5=39;c.pin_d6=34;c.pin_d7=35;
  c.pin_xclk=0;c.pin_pclk=22;c.pin_vsync=25;c.pin_href=23;c.pin_sccb_sda=26;c.pin_sccb_scl=27;c.pin_pwdn=32;c.pin_reset=-1;
  c.xclk_freq_hz=20000000;c.pixel_format=PIXFORMAT_JPEG;c.frame_size=FRAMESIZE_VGA;
  c.jpeg_quality=12;c.fb_count=2;c.grab_mode=CAMERA_GRAB_LATEST;c.fb_location=CAMERA_FB_IN_PSRAM;
  esp_log_level_set("*",ESP_LOG_WARN);
  cameraError=psramFound()?esp_camera_init(&c):ESP_ERR_NO_MEM;
  esp_log_level_set("*",ESP_LOG_NONE);
  cameraReady=cameraError==ESP_OK;
}
void loop() {
  while(Serial.available()){
    char c=(char)Serial.read();
    if(c=='\r')continue;
    if(c=='\n'){
      if(overflow)error("","COMMAND_TOO_LONG");
      else if(used){input[used]=0;command(input);}
      memset(input,0,sizeof(input));used=0;overflow=false;
    }else if(used<sizeof(input)-1)input[used++]=c;else overflow=true;
  }
  previewTick();
  delay(2);
}
