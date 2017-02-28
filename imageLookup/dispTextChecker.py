#!/usr/bin/env python
import textChecker
import pygame
import sys
import adGlobal
import syslog
import time
debug = False


pygame.init()
pygame.mouse.set_visible(False);
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
myfont = pygame.font.Font(adGlobal.fontDir + "/Watchword_bold_demo.otf", 200)

def printText(text):
    global screen
    global myfont
    # render text
    lineSpacing = adGlobal.lineSpacing
    label1 = myfont.render(text[0], 1, (255,255,0))
    label2 = myfont.render(text[1], 1, (255,255,0))
    maxWidth = max(label1.get_width(),label2.get_width())
    maxHeight = label1.get_height() + label2.get_height() + lineSpacing 
    wordRect = pygame.Surface((maxWidth,maxHeight))
    screen.fill((0,0,0));
    if maxWidth == label1.get_width():
        wordRect.blit(label1, (0, 0))
        offset = (maxWidth - label2.get_width()) / 2
        wordRect.blit(label2, (offset, label1.get_height() + lineSpacing))
    else:
        offset = (maxWidth - label1.get_width()) / 2
        wordRect.blit(label1, (offset, 0))
        wordRect.blit(label2, (0, label1.get_height() + lineSpacing))

    wx = (screen.get_width() - wordRect.get_width()) / 2
    if wx < 0: 
        wx = 0
    wy = (screen.get_height() - wordRect.get_height()) / 2
    if wy < 0:
        wy = 0
    screen.blit(wordRect,(wx,wy)) 
    pygame.display.flip() 

def dispTextChecker():
    imageDir=adGlobal.imageDir
    count=0
    syslog.syslog("disp text checker started successfully")
    while True:
        if debug: 
            count += 1
            syslog.syslog( "disp text checking for text. count:"+str(count) )
        text = textChecker.getText();
        if text == None:
            if debug:
                syslog.syslog( "disp text no text" )
        else:
            if debug:
                syslog.syslog("disp text found text:"+str(text))
            printText(text)
        time.sleep(5)


if __name__ == '__main__':
      dispTextChecker()
