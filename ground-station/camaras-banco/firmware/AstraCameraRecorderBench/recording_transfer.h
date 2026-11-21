// ASTRA-39: lectura acotada de archivos del banco; no recibe rutas arbitrarias ni escribe SD.
static bool recordingTransferCommand(char *line){
  if(strncmp(line,"REC_READ",8))return false;
  char verb[12]={},id[17]={},boot[17]={},origin[17]={},run[17]={},kind[2]={},seg[5]={},frame[3]={},extra[2]={};
  int count=sscanf(line,"%11s %16s %16s %16s %16s %1s %4s %2s %1s",verb,id,boot,origin,run,kind,seg,frame,extra);
  if(!recordingHex(id)){error("","BAD_ID");return true;}
  if(strcmp(verb,"REC_READ") || count!=8 || strcmp(boot,bootId) || !recordingHex(origin) || !recordingHex(run)){
    error(id,"BAD_READ_ARGUMENTS_OR_BOOT");return true;
  }
  if(recordRunning || previewOn){error(id,"READ_REQUIRES_IDLE_AND_WIFI_OFF");return true;}
  bool digits=strlen(seg)>0 && strlen(frame)>0;
  for(unsigned i=0;i<strlen(seg);i++)if(!isdigit((unsigned char)seg[i]))digits=false;
  for(unsigned i=0;i<strlen(frame);i++)if(!isdigit((unsigned char)frame[i]))digits=false;
  unsigned si=digits?atoi(seg):9999,fi=digits?atoi(frame):99;
  if(!digits || si>600 || fi>60 || !strchr("SRMJI",kind[0])){error(id,"READ_SELECTOR_INVALID");return true;}
  bool top=kind[0]=='S' || kind[0]=='R';
  if((top && (si || fi)) || (!top && !si) || (kind[0]=='M' && fi) || ((kind[0]=='J' || kind[0]=='I') && !fi)){
    error(id,"READ_SELECTOR_INVALID");return true;
  }
  // Origen de carpeta explicito y hexadecimal; nunca acepto una ruta arbitraria.
  char path[180],base[100];snprintf(base,sizeof(base),"/ASTRA_REC_%s_%s",origin,run);
  if(kind[0]=='S')snprintf(path,sizeof(path),"%s/session-start.json",base);
  else if(kind[0]=='R')snprintf(path,sizeof(path),"%s/session-result.json",base);
  else if(kind[0]=='M')snprintf(path,sizeof(path),"%s/segment_%04u/sequence.json",base,si);
  else snprintf(path,sizeof(path),"%s/segment_%04u/frame_%04u.%s",base,si,fi,kind[0]=='J'?"jpg":"json");
  if(!SD_MMC.begin("/sdcard",true,false)){error(id,"READ_MOUNT_FAILED");return true;}
  File f=SD_MMC.open(path,FILE_READ);
  size_t limit=kind[0]=='J'?512*1024:128*1024;
  if(!f || f.isDirectory() || !f.size() || f.size()>limit){if(f)f.close();SD_MMC.end();error(id,"READ_FILE_NOT_FOUND_OR_TOO_LARGE");return true;}
  size_t length=f.size(),read=0;uint32_t sum=0xffffffffU;uint8_t block[512];
  while(f.available()){size_t n=f.read(block,sizeof(block));if(!n)break;sum=crc32data(block,n,sum);read+=n;}
  if(read!=length || !f.seek(0)){f.close();SD_MMC.end();error(id,"READ_FAILED");return true;}
  Serial.printf("@CAM {\"v\":1,\"event\":\"file\",\"id\":\"%s\",\"boot\":\"%s\",\"device\":\"%s\",\"length\":%u,\"crc32\":\"%08lx\"}\n",id,bootId,deviceId,(unsigned)length,(unsigned long)(sum^0xffffffffU));
  size_t sent=0;
  while(sent<length){size_t n=f.read(block,min(sizeof(block),length-sent));if(!n)break;Serial.write(block,n);sent+=n;}
  Serial.flush();f.close();SD_MMC.end();
  Serial.printf("\n@CAM {\"v\":1,\"event\":\"file_end\",\"id\":\"%s\",\"boot\":\"%s\",\"sent\":%u}\n",id,bootId,(unsigned)sent);
  return true;
}
