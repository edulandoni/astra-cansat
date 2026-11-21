// ASTRA-39: ensayo breve de banco; no implemento interfaz ni estado de vuelo.
// Requiere las funciones/identidades de la copia local de AstraCameraBench.
struct SequenceFrame { int64_t timestamp; uint32_t length; uint32_t crc; };

bool sequenceReadback(const char *path,size_t expected,uint32_t crc) {
  File f=SD_MMC.open(path,FILE_READ);if(!f)return false;
  uint8_t bytes[512];uint32_t sum=0xffffffffU;size_t total=0;
  while(f.available()) {size_t n=f.read(bytes,sizeof(bytes));if(!n)break;sum=crc32data(bytes,n,sum);total+=n;}
  f.close();return total==expected && (sum^0xffffffffU)==crc;
}

void sequenceClip(const char *id) {
  const unsigned target=12;const int64_t period=500000;
  if(!cameraReady){error(id,"CAMERA_INIT_FAILED");return;}
  pinMode(4,OUTPUT);digitalWrite(4,LOW);
  if(!SD_MMC.begin("/sdcard",true,false)){error(id,"SEQUENCE_MOUNT_FAILED");return;}
  char directory[96];snprintf(directory,sizeof(directory),"/ASTRA_SEQ_%s_%s",bootId,id);
  if(SD_MMC.exists(directory)){SD_MMC.end();error(id,"SEQUENCE_EXISTS_REFUSED");return;}
  const uint64_t reserve=(uint64_t)target*512*1024+128*1024;
  if(SD_MMC.totalBytes()<SD_MMC.usedBytes() || SD_MMC.totalBytes()-SD_MMC.usedBytes()<reserve){
    SD_MMC.end();error(id,"SEQUENCE_SPACE_INSUFFICIENT");return;
  }
  if(!SD_MMC.mkdir(directory)){SD_MMC.end();error(id,"SEQUENCE_DIRECTORY_FAILED");return;}
  char path[128];snprintf(path,sizeof(path),"%s/started.json",directory);
  File started=SD_MMC.open(path,FILE_WRITE);
  if(!started){SD_MMC.end();error(id,"SEQUENCE_START_FAILED");return;}
  started.printf("{\"profile\":\"camera-sequence-0.1\",\"id\":\"%s\",\"boot\":\"%s\",\"device\":\"%s\",\"expected_frames\":%u,\"target_interval_us\":%lld}",id,bootId,deviceId,target,(long long)period);
  started.flush();bool startOk=!started.getWriteError();started.close();
  if(!startOk){SD_MMC.end();error(id,"SEQUENCE_START_WRITE_FAILED");return;}
  SequenceFrame frames[target];unsigned count=0;const char *reason="COMPLETE";
  int64_t request=esp_timer_get_time(),next=request;
  // Libero imágenes pendientes antes de iniciar la secuencia solicitada.
  for(int i=0;i<2;i++) {
    camera_fb_t *old=esp_camera_fb_get();
    if(!old){reason="WARMUP_FAILED";break;}
    esp_camera_fb_return(old);delay(80);
  }
  if(!strcmp(reason,"COMPLETE"))for(unsigned index=1;index<=target;index++) {
    while(esp_timer_get_time()<next)delay(2);
    camera_fb_t *fb=esp_camera_fb_get();
    if(!fb){reason="FRAME_FAILED";break;}
    int64_t stamp=(int64_t)fb->timestamp.tv_sec*1000000+fb->timestamp.tv_usec;
    if(stamp<request || (count && stamp<=frames[count-1].timestamp)) {
      esp_camera_fb_return(fb);reason="STALE_OR_REPEATED_FRAME";break;
    }
    if(fb->format!=PIXFORMAT_JPEG || fb->width!=640 || fb->height!=480 || fb->len<4 || fb->len>512*1024 || fb->buf[0]!=0xff || fb->buf[1]!=0xd8 || fb->buf[fb->len-2]!=0xff || fb->buf[fb->len-1]!=0xd9) {
      esp_camera_fb_return(fb);reason="INVALID_JPEG";break;
    }
    uint32_t crc=crc32data(fb->buf,fb->len)^0xffffffffU;size_t length=fb->len;
    snprintf(path,sizeof(path),"%s/frame_%04u.jpg",directory,index);
    if(SD_MMC.exists(path)){esp_camera_fb_return(fb);reason="FRAME_EXISTS_REFUSED";break;}
    File f=SD_MMC.open(path,FILE_WRITE);
    if(!f){esp_camera_fb_return(fb);reason="FRAME_OPEN_FAILED";break;}
    size_t written=f.write(fb->buf,length);f.flush();bool writeOk=written==length && !f.getWriteError();f.close();
    esp_camera_fb_return(fb);
    if(!writeOk){reason="FRAME_WRITE_FAILED";break;}
    if(!sequenceReadback(path,length,crc)){reason="FRAME_READBACK_FAILED";break;}
    frames[count++]={stamp,(uint32_t)length,crc};
    // Sidecar inmutable por cuadro: conserva tiempo/CRC aunque falte el cierre.
    snprintf(path,sizeof(path),"%s/frame_%04u.json",directory,index);
    File sidecar=SD_MMC.open(path,FILE_WRITE);
    if(!sidecar){reason="SIDECAR_OPEN_FAILED";break;}
    sidecar.printf("{\"index\":%u,\"boot\":\"%s\",\"capture_us\":%lld,\"bytes\":%u,\"crc32\":\"%08lx\"}",index,bootId,(long long)stamp,(unsigned)length,(unsigned long)crc);
    sidecar.flush();bool sidecarOk=!sidecar.getWriteError();sidecar.close();
    if(!sidecarOk){reason="SIDECAR_WRITE_FAILED";break;}
    // El tiempo real de captura/escritura manda. No recupero retraso en ráfagas.
    next=esp_timer_get_time()+period;
  }
  bool complete=count==target && !strcmp(reason,"COMPLETE");
  snprintf(path,sizeof(path),"%s/sequence.json",directory);
  File manifest=SD_MMC.open(path,FILE_WRITE);bool manifestOk=false;
  if(manifest) {
    manifest.printf("{\"v\":1,\"profile\":\"camera-sequence-0.1\",\"origin\":\"camera\",\"boot\":\"%s\",\"device\":\"%s\",\"expected_frames\":%u,\"closed\":%s,\"reason\":\"%s\",\"frames\":[",bootId,deviceId,target,complete?"true":"false",reason);
    for(unsigned i=0;i<count;i++)manifest.printf("%s{\"index\":%u,\"file\":\"frame_%04u.jpg\",\"boot\":\"%s\",\"capture_us\":%lld,\"bytes\":%u,\"crc32\":\"%08lx\"}",i?",":"",i+1,i+1,bootId,(long long)frames[i].timestamp,frames[i].length,(unsigned long)frames[i].crc);
    manifest.print("]}");manifest.flush();manifestOk=!manifest.getWriteError();manifest.close();
  }
  SD_MMC.end();
  Serial.printf("@CAM {\"v\":1,\"event\":\"sequence\",\"id\":\"%s\",\"boot\":\"%s\",\"device\":\"%s\",\"path\":\"%s\",\"frames\":%u,\"expected_frames\":%u,\"closed\":%s,\"reason\":\"%s\"}\n",id,bootId,deviceId,directory,count,target,complete && manifestOk?"true":"false",manifestOk?reason:"MANIFEST_WRITE_FAILED");
}
