// ASTRA-39: mantenimiento local. Un solo productor de imagen; red no controla potencia.
#include <WiFi.h>
#include "esp_http_server.h"
#include "esp_heap_caps.h"

static httpd_handle_t previewServer=nullptr;
static SemaphoreHandle_t previewMutex=nullptr;
static uint8_t *previewBytes=nullptr;
static size_t previewLength=0;
static uint64_t previewIndex=0;
static int64_t previewStamp=0;
static volatile bool previewOn=false;
static bool previewClient=false;
static int64_t previewNext=0;
static const size_t previewLimit=512*1024;

static esp_err_t previewStream(httpd_req_t *req) {
  // Atiendo un solo flujo. Copio a PSRAM antes de enviar; la red no retiene el buffer de captura.
  if(previewClient){httpd_resp_set_status(req,"503 Service Unavailable");httpd_resp_send(req,"BUSY",4);return ESP_FAIL;}
  uint8_t *copy=(uint8_t*)heap_caps_malloc(previewLimit,MALLOC_CAP_SPIRAM|MALLOC_CAP_8BIT);
  if(!copy){httpd_resp_send_err(req,HTTPD_500_INTERNAL_SERVER_ERROR,"NO_MEMORY");return ESP_FAIL;}
  previewClient=true;
  httpd_resp_set_type(req,"multipart/x-mixed-replace; boundary=astra-frame");
  httpd_resp_set_hdr(req,"Cache-Control","no-store");
  uint64_t previous=0;esp_err_t result=ESP_OK;
  while(previewOn) {
    size_t length=0;uint64_t index=0;int64_t stamp=0;
    if(xSemaphoreTake(previewMutex,pdMS_TO_TICKS(50))==pdTRUE){
      if(previewIndex!=previous && previewLength){length=previewLength;index=previewIndex;stamp=previewStamp;memcpy(copy,previewBytes,length);}
      xSemaphoreGive(previewMutex);
    }
    if(!length){vTaskDelay(pdMS_TO_TICKS(10));continue;}
    char header[300];int n=snprintf(header,sizeof(header),"--astra-frame\r\nContent-Type: image/jpeg\r\nContent-Length: %u\r\nX-Device: %s\r\nX-Boot: %s\r\nX-Frame-Id: %llu\r\nX-Capture-Us: %lld\r\n\r\n",(unsigned)length,deviceId,bootId,(unsigned long long)index,(long long)stamp);
    if(n<=0 || (size_t)n>=sizeof(header)){result=ESP_FAIL;break;}
    if((result=httpd_resp_send_chunk(req,header,n))!=ESP_OK)break;
    if((result=httpd_resp_send_chunk(req,(const char*)copy,length))!=ESP_OK)break;
    if((result=httpd_resp_send_chunk(req,"\r\n",2))!=ESP_OK)break;
    previous=index;
  }
  free(copy);previewClient=false;
  return result;
}

static void previewStop() {
  previewOn=false;
  if(previewServer){httpd_stop(previewServer);previewServer=nullptr;}
  WiFi.softAPdisconnect(true);WiFi.mode(WIFI_OFF);
  // Conservo el buffer y mutex hasta el reinicio; sólo se reserva uno.
  if(previewMutex && xSemaphoreTake(previewMutex,pdMS_TO_TICKS(100))==pdTRUE){previewLength=0;xSemaphoreGive(previewMutex);}
}

static bool previewCommand(char *line) {
  // Los comandos existentes usan 16 hex como correlacion; agrego WIFI_ON id clave-hex16.
  if(strncmp(line,"WIFI_",5))return false;
  char verb[16]={},id[17]={},password[17]={},extra[2]={};
  int count=sscanf(line,"%15s %16s %16s %1s",verb,id,password,extra);
  bool idOk=strlen(id)==16;
  for(size_t i=0;i<strlen(id);i++)if(!isxdigit((unsigned char)id[i]))idOk=false;
  if(!idOk){error("","BAD_ID");return true;}
  if(!strcmp(verb,"WIFI_OFF") && count==2){previewStop();Serial.printf("@CAM {\"event\":\"wifi_off\",\"id\":\"%s\",\"boot\":\"%s\"}\n",id,bootId);return true;}
  bool keyOk=count==3 && strlen(password)==16;
  for(size_t i=0;i<strlen(password);i++)if(!isxdigit((unsigned char)password[i]))keyOk=false;
  if(strcmp(verb,"WIFI_ON") || !keyOk){error(id,"BAD_WIFI_COMMAND");return true;}
  if(previewOn){error(id,"WIFI_ALREADY_ACTIVE");return true;}
  if(!cameraReady){error(id,"CAMERA_INIT_FAILED");return true;}
  if(!previewMutex)previewMutex=xSemaphoreCreateMutex();
  if(!previewBytes)previewBytes=(uint8_t*)heap_caps_malloc(previewLimit,MALLOC_CAP_SPIRAM|MALLOC_CAP_8BIT);
  if(!previewMutex || !previewBytes){error(id,"PREVIEW_MEMORY_FAILED");return true;}
  char ssid[32];snprintf(ssid,sizeof(ssid),"ASTRA-CAM-%.6s",bootId+10);
  WiFi.mode(WIFI_AP);
  if(!WiFi.softAP(ssid,password,1,false,1)){previewStop();error(id,"AP_START_FAILED");return true;}
  memset(password,0,sizeof(password));
  httpd_config_t cfg=HTTPD_DEFAULT_CONFIG();cfg.server_port=81;cfg.ctrl_port=32769;cfg.max_open_sockets=2;cfg.send_wait_timeout=1;cfg.recv_wait_timeout=1;cfg.lru_purge_enable=true;
  if(httpd_start(&previewServer,&cfg)!=ESP_OK){previewStop();error(id,"HTTP_START_FAILED");return true;}
  httpd_uri_t route={};route.uri="/stream";route.method=HTTP_GET;route.handler=previewStream;
  if(httpd_register_uri_handler(previewServer,&route)!=ESP_OK){previewStop();error(id,"HTTP_ROUTE_FAILED");return true;}
  previewOn=true;previewNext=0;
  Serial.printf("@CAM {\"event\":\"wifi_ready\",\"id\":\"%s\",\"boot\":\"%s\",\"ssid\":\"%s\",\"ip\":\"%s\",\"recording_verified\":false}\n",id,bootId,ssid,WiFi.softAPIP().toString().c_str());
  return true;
}

static void previewTick() {
  if(!previewOn || !cameraReady || esp_timer_get_time()<previewNext)return;
  previewNext=esp_timer_get_time()+100000; // Objetivo de banco, no fps garantizado.
  camera_fb_t *fb=esp_camera_fb_get();if(!fb)return;
  int64_t stamp=(int64_t)fb->timestamp.tv_sec*1000000+fb->timestamp.tv_usec;
  if(fb->format==PIXFORMAT_JPEG && fb->len>=4 && fb->len<=previewLimit && stamp>previewStamp && fb->buf[0]==0xff && fb->buf[1]==0xd8 && fb->buf[fb->len-2]==0xff && fb->buf[fb->len-1]==0xd9){
    if(xSemaphoreTake(previewMutex,pdMS_TO_TICKS(50))==pdTRUE){memcpy(previewBytes,fb->buf,fb->len);previewLength=fb->len;previewStamp=stamp;previewIndex++;xSemaphoreGive(previewMutex);}
  }
  esp_camera_fb_return(fb);
}
