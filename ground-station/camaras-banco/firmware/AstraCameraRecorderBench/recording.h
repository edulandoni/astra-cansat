// ASTRA-39/24: banco local. Grabacion independiente del seguimiento USB.
static const unsigned recordSegmentLimit=60;
static const int64_t recordPeriod=200000; // Objetivo 5 Hz, no prestacion garantizada.
static SequenceFrame recordFrames[recordSegmentLimit];
static bool recordRunning=false,recordMounted=false,recordSegmentOpen=false;
static char recordRun[17]="",recordDirectory[96]="",recordSegment[128]="";
static char recordState[20]="IDLE",recordReason[48]="",recordError[48]="";
static char recordSeen[8][17]={};static unsigned recordSeenNext=0;
static unsigned recordCount=0,recordSegments=0,recordCaptured=0,recordWritten=0;
static unsigned recordRequestedSeconds=0;
static uint64_t recordBytes=0,recordFree=0,recordReport=0;
static int64_t recordStarted=0,recordDeadline=0,recordNext=0,recordLastCapture=0,recordLastWrite=0;

static bool recordingActive(){return recordRunning;}
static bool recordingHex(const char *s){if(strlen(s)!=16)return false;for(unsigned i=0;i<16;i++)if(!isxdigit((unsigned char)s[i]))return false;return true;}

static void recordingStatus(const char *id){
  Serial.printf("@CAM {\"v\":1,\"event\":\"recorder\",\"profile\":\"camera-recorder-0.1\",\"id\":\"%s\",\"device\":\"%s\",\"boot\":\"%s\",\"run\":\"%s\",\"segment\":\"%s\",\"state\":\"%s\",\"recording\":%s,\"report_seq\":%llu,\"frames_captured\":%u,\"frames_written\":%u,\"frames_readback\":%u,\"bytes_written\":%llu,\"uptime_ms\":%lld,\"last_write_ms\":%lld,\"free_bytes\":%llu,\"segments_closed\":%u,\"path\":\"%s\",\"reason\":\"%s\",\"error\":\"%s\"}\n",
    id,deviceId,bootId,recordRun,recordSegment[0]?recordSegment:"idle",recordState,recordRunning?"true":"false",(unsigned long long)++recordReport,recordCaptured,recordWritten,recordWritten,(unsigned long long)recordBytes,(long long)(esp_timer_get_time()/1000),(long long)(recordLastWrite/1000),(unsigned long long)recordFree,recordSegments,recordDirectory,recordReason,recordError);
}

static bool recordingText(const char *path,const char *text){
  if(SD_MMC.exists(path))return false;
  File f=SD_MMC.open(path,FILE_WRITE);if(!f)return false;
  size_t length=strlen(text),n=f.write((const uint8_t*)text,length);f.flush();bool ok=n==length && !f.getWriteError();f.close();
  return ok && sequenceReadback(path,length,crc32data((const uint8_t*)text,length)^0xffffffffU);
}

static bool recordingCloseSegment(bool complete){
  if(!recordSegmentOpen)return true;
  char path[160];snprintf(path,sizeof(path),"%s/sequence.json",recordSegment);
  if(SD_MMC.exists(path))return false;
  File f=SD_MMC.open(path,FILE_WRITE);if(!f)return false;
  f.printf("{\"v\":1,\"profile\":\"camera-sequence-0.1\",\"origin\":\"camera\",\"boot\":\"%s\",\"device\":\"%s\",\"expected_frames\":%u,\"closed\":%s,\"reason\":\"%s\",\"frames\":[",bootId,deviceId,recordCount,complete?"true":"false",complete?"COMPLETE":"RECORDING_ERROR");
  for(unsigned i=0;i<recordCount;i++)f.printf("%s{\"index\":%u,\"file\":\"frame_%04u.jpg\",\"boot\":\"%s\",\"capture_us\":%lld,\"bytes\":%u,\"crc32\":\"%08lx\"}",i?",":"",i+1,i+1,bootId,(long long)recordFrames[i].timestamp,recordFrames[i].length,(unsigned long)recordFrames[i].crc);
  f.print("]}");f.flush();bool ok=!f.getWriteError();f.close();
  if(ok){recordSegmentOpen=false;if(complete)recordSegments++;}
  return ok;
}

static void recordingFinish(const char *reason,bool success){
  recordRunning=false;strlcpy(recordState,"CLOSING",sizeof(recordState));
  strlcpy(recordReason,reason,sizeof(recordReason));
  if(!recordWritten && success){success=false;strlcpy(recordReason,"NO_VERIFIED_FRAMES",sizeof(recordReason));}
  if(!recordingCloseSegment(success)){success=false;strlcpy(recordReason,"SEGMENT_CLOSE_FAILED",sizeof(recordReason));}
  char path[160],text[700];snprintf(path,sizeof(path),"%s/session-result.json",recordDirectory);
  snprintf(text,sizeof(text),"{\"v\":1,\"profile\":\"camera-recording-0.1\",\"origin\":\"camera\",\"device\":\"%s\",\"boot\":\"%s\",\"run\":\"%s\",\"closed\":%s,\"reason\":\"%s\",\"segments_closed\":%u,\"frames_captured\":%u,\"frames_written\":%u,\"bytes_written\":%llu,\"started_us\":%lld,\"finished_us\":%lld}",deviceId,bootId,recordRun,success?"true":"false",recordReason,recordSegments,recordCaptured,recordWritten,(unsigned long long)recordBytes,(long long)recordStarted,(long long)esp_timer_get_time());
  if(!recordingText(path,text)){success=false;strlcpy(recordReason,"SESSION_CLOSE_FAILED",sizeof(recordReason));}
  if(recordMounted){SD_MMC.end();recordMounted=false;}
  strlcpy(recordState,success?"COMPLETE":"FAILED",sizeof(recordState));
  if(!success)strlcpy(recordError,recordReason,sizeof(recordError));
}

static void recordingStart(const char *id,unsigned seconds){
  if(!strcmp(id,recordRun)){if(seconds!=recordRequestedSeconds)error(id,"RUN_ARGUMENT_CONFLICT");else recordingStatus(id);return;}
  for(unsigned i=0;i<8;i++)if(!strcmp(id,recordSeen[i])){error(id,"RUN_ALREADY_USED");return;}
  if(recordRunning){error(id,"RECORDING_BUSY");return;}
  if(previewOn){error(id,"WIFI_MUST_BE_OFF");return;}
  if(!cameraReady){error(id,"CAMERA_INIT_FAILED");return;}
  strlcpy(recordSeen[recordSeenNext++%8],id,17);strlcpy(recordRun,id,sizeof(recordRun));
  recordRequestedSeconds=seconds;
  recordCaptured=recordWritten=recordSegments=recordCount=0;recordBytes=recordFree=0;
  recordLastWrite=recordLastCapture=0;recordSegment[0]=0;recordError[0]=0;recordReason[0]=0;recordSegmentOpen=false;
  recordStarted=esp_timer_get_time();recordDeadline=recordStarted+(int64_t)seconds*1000000;
  recordNext=recordStarted;snprintf(recordDirectory,sizeof(recordDirectory),"/ASTRA_REC_%s_%s",bootId,id);
  if(!SD_MMC.begin("/sdcard",true,false)){strlcpy(recordState,"FAILED",sizeof(recordState));strlcpy(recordError,"MOUNT_FAILED",sizeof(recordError));recordingStatus(id);return;}
  recordMounted=true;
  if(SD_MMC.exists(recordDirectory) || !SD_MMC.mkdir(recordDirectory)){
    SD_MMC.end();recordMounted=false;strlcpy(recordState,"FAILED",sizeof(recordState));strlcpy(recordError,"SESSION_DIRECTORY_REFUSED",sizeof(recordError));recordingStatus(id);return;
  }
  char path[160],text[650];snprintf(path,sizeof(path),"%s/session-start.json",recordDirectory);
  snprintf(text,sizeof(text),"{\"v\":1,\"profile\":\"camera-recording-0.1\",\"origin\":\"camera\",\"device\":\"%s\",\"boot\":\"%s\",\"run\":\"%s\",\"requested_seconds\":%u,\"started_us\":%lld,\"target_interval_us\":%lld,\"segment_limit\":%u}",deviceId,bootId,id,seconds,(long long)recordStarted,(long long)recordPeriod,recordSegmentLimit);
  if(!recordingText(path,text)){strlcpy(recordError,"SESSION_START_FAILED",sizeof(recordError));recordingFinish("SESSION_START_FAILED",false);recordingStatus(id);return;}
  recordRunning=true;strlcpy(recordState,"RECORDING",sizeof(recordState));recordingStatus(id);
}

static bool recordingCommand(char *line){
  if(strncmp(line,"REC_",4))return false;
  char verb[16]={},id[17]={},boot[17]={},arg[20]={},extra[2]={};
  int count=sscanf(line,"%15s %16s %16s %19s %1s",verb,id,boot,arg,extra);
  if(!recordingHex(id)){error("","BAD_ID");return true;}
  if(!strcmp(verb,"REC_STATUS") && count==2){recordingStatus(id);return true;}
  if(count!=4 || strcmp(boot,bootId)){error(id,"BAD_ARGUMENTS_OR_BOOT");return true;}
  if(!strcmp(verb,"REC_START")){
    bool digits=strlen(arg)>0;for(unsigned i=0;i<strlen(arg);i++)if(!isdigit((unsigned char)arg[i]))digits=false;
    unsigned long seconds=digits?strtoul(arg,nullptr,10):0;
    if(seconds<1 || seconds>3600){error(id,"DURATION_OUT_OF_RANGE");return true;}
    recordingStart(id,(unsigned)seconds);return true;
  }
  if(!strcmp(verb,"REC_STOP")){
    if(!recordingHex(arg) || strcmp(arg,recordRun)){error(id,"RUN_MISMATCH");return true;}
    if(recordRunning)recordingFinish("STOP_REQUESTED",true);
    recordingStatus(id);return true;
  }
  error(id,"UNKNOWN_RECORDER_COMMAND");return true;
}

static void recordingTick(){
  if(!recordRunning)return;
  int64_t now=esp_timer_get_time();
  if(now>=recordDeadline){recordingFinish("DURATION_LIMIT",true);return;}
  if(now<recordNext)return;
  recordNext=now+recordPeriod; // No acumulo cuadros para recuperar un atraso en rafagas.
  camera_fb_t *fb=esp_camera_fb_get();
  if(!fb){recordingFinish("FRAME_FAILED",false);return;}
  int64_t stamp=(int64_t)fb->timestamp.tv_sec*1000000+fb->timestamp.tv_usec;
  if(stamp<recordStarted){esp_camera_fb_return(fb);return;} // Descarto cuadros anteriores al inicio.
  if(fb->format!=PIXFORMAT_JPEG || fb->width!=640 || fb->height!=480 || fb->len<4 || fb->len>512*1024 || fb->buf[0]!=0xff || fb->buf[1]!=0xd8 || fb->buf[fb->len-2]!=0xff || fb->buf[fb->len-1]!=0xd9 || stamp<=recordLastCapture){
    esp_camera_fb_return(fb);recordingFinish("INVALID_OR_STALE_FRAME",false);return;
  }
  recordCaptured++;recordLastCapture=stamp;
  uint64_t total=SD_MMC.totalBytes(),usedBytes=SD_MMC.usedBytes();recordFree=total>=usedBytes?total-usedBytes:0;
  if(recordFree<(uint64_t)fb->len+64*1024){esp_camera_fb_return(fb);recordingFinish("SPACE_INSUFFICIENT",false);return;}
  if(!recordSegmentOpen){
    recordCount=0;snprintf(recordSegment,sizeof(recordSegment),"%s/segment_%04u",recordDirectory,recordSegments+1);
    if(SD_MMC.exists(recordSegment) || !SD_MMC.mkdir(recordSegment)){esp_camera_fb_return(fb);recordingFinish("SEGMENT_DIRECTORY_REFUSED",false);return;}
    recordSegmentOpen=true;
  }
  unsigned index=recordCount+1;char path[160];snprintf(path,sizeof(path),"%s/frame_%04u.jpg",recordSegment,index);
  if(SD_MMC.exists(path)){esp_camera_fb_return(fb);recordingFinish("FRAME_EXISTS_REFUSED",false);return;}
  uint32_t length=fb->len,crc=crc32data(fb->buf,fb->len)^0xffffffffU;
  File f=SD_MMC.open(path,FILE_WRITE);if(!f){esp_camera_fb_return(fb);recordingFinish("FRAME_OPEN_FAILED",false);return;}
  size_t n=f.write(fb->buf,length);f.flush();bool ok=n==length && !f.getWriteError();f.close();esp_camera_fb_return(fb);
  if(!ok || !sequenceReadback(path,length,crc)){recordingFinish("FRAME_WRITE_OR_READBACK_FAILED",false);return;}
  char text[260];snprintf(path,sizeof(path),"%s/frame_%04u.json",recordSegment,index);
  snprintf(text,sizeof(text),"{\"index\":%u,\"boot\":\"%s\",\"capture_us\":%lld,\"bytes\":%u,\"crc32\":\"%08lx\"}",index,bootId,(long long)stamp,length,(unsigned long)crc);
  if(!recordingText(path,text)){recordingFinish("SIDECAR_WRITE_FAILED",false);return;}
  recordFrames[recordCount++]={stamp,length,crc};recordWritten++;recordBytes+=length;recordLastWrite=esp_timer_get_time();
  if(recordCount==recordSegmentLimit && !recordingCloseSegment(true))recordingFinish("SEGMENT_CLOSE_FAILED",false);
}
