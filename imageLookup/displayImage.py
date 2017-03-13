#!/usr/bin/env python
import textChecker
import pygame
import sys
import adGlobal
import syslog
import time
debug = True

screen=None
setupDone=False

def setup():
  global screen
  global setupDone
  if setupDone:
      return
  pygame.init()
  pygame.mouse.set_visible(False);
  screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
  setupDone=True
  syslog.syslog("display image setup done")

def displayImage(img):
  global screen
  global setupDone
  setup()
  try:
    image = pygame.image.load(img);
  except:
    syslog.syslog("display Image can't render "+img)
    image = pygame.image.load(adGlobal.defaultImg)
    return;
  ws=screen.get_width()
  hs=screen.get_height()
  rs = float(ws)/float(hs)
  wi = image.get_width()
  hi = image.get_height()
  ri = float(wi)/float(hi)
  dw = 0
  dh = 0
  if  wi < (ws/2) and hi < (hs/2):
    syslog.syslog("doing half scale:"+img)
    simage = pygame.transform.scale2x(image)
  else:
    if rs > ri:
      dw = wi * (float(hs)/float(hi))
      dh = hs
    else:
      dw = ws
      dh = hi * (float(ws)/float(wi))

    try:
      syslog.syslog("doing smooth scale:"+img)
      simage = pygame.transform.smoothscale(image,(int(dw),int(dh)))
    except:
      syslog.syslog("smoothscale failed doing normal scale for:"+img)
      simage = pygame.transform.scale(image,(int(dw),int(dh)))

  xoffset = (ws - simage.get_width()) / 2
  yoffset = (hs - simage.get_height()) / 2
  if debug: syslog.syslog("displayImage ws:"+str(ws) 
          + " hs:"+str(hs) 
          + " rs:"+str(rs)
          +"  wi:"+str(wi) 
          + " hi:"+str(hi) 
          + " ri:"+str(ri) 
          + " dw:"+str(dw) 
          + " dh:"+str(dh) 
          + " xoffset:"+str(xoffset) 
          + " yoffset:"+str(yoffset) 
          )
  screen.fill((0,0,0))
  screen.blit(simage,(xoffset,yoffset)) 
  pygame.display.flip() 


if __name__ == '__main__':
    displayImage(sys.argv[1])
    time.sleep(5)
    
	
