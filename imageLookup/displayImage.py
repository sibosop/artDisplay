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
    # render text
    try:
        image = pygame.image.load(img);
    except:
        syslog.syslog("display Image can't render "+img)
        return;
    sw=screen.get_width()
    sh=screen.get_height()
    iw = image.get_width()
    ih = image.get_height()
    iratio = float(iw) / float(ih)
    dw = iratio * sh
    

    simage = pygame.transform.scale(image,(int(dw),sh))
    xoffset = (sw - simage.get_width()) / 2
    if debug: syslog.syslog("displayImage sw:"+str(sw) 
            + " sh:"+str(sh) 
            + " ratio:"+str(iratio)
            +" iw:"+str(iw) 
            + " ih:"+str(ih) 
            + " xoffset:"+str(xoffset) 
            + " dw:"+str(dw))
    screen.fill((0,0,0));
    screen.blit(simage,(xoffset,0)) 
    pygame.display.flip() 


if __name__ == '__main__':
    displayImage(sys.argv[1])
    time.sleep(5)
    
	
