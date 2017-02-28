#!/bin/python
import pygame
import sys

if len(sys.argv) != 3:
    sys.exit("needs two strings");
pygame.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
done = False



pygame.mouse.set_visible(False);
while not done:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True

    # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
    myfont = pygame.font.Font("../../fonts/Watchword_bold_demo.otf", 200)

    # render text
    lineSpacing = 20
    label1 = myfont.render(sys.argv[1], 1, (255,255,0))
    label2 = myfont.render(sys.argv[2], 1, (255,255,0))
    maxWidth = max(label1.get_width(),label2.get_width())
    maxHeight = label1.get_height() + label2.get_height() + lineSpacing 
    wordRect = pygame.Surface((maxWidth,maxHeight))
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
