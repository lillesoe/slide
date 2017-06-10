import sys 
import pygame.image
import pygame.display
import fnmatch
import os
import random
import time
import re

#Get the size of the display
pygame.display.init()
#Hide the mouse
pygame.mouse.set_visible(0)
info = pygame.display.Info()
print info
max_y = info.current_h
max_x = info.current_w

#Directory can be specified in commandline else below is the default
dir = "/mnt/gallery/"
if len(sys.argv)==2:
    dir = sys.argv[1]
print "Using directory: " + dir

#We want this to run forever - and maybe some new images
while (1) :
  print "Finding files"

  #Get all the paths for images
  files = []
  size = 0
  for root, dirnames, filenames in os.walk(dir):
    for filename in fnmatch.filter(filenames, '*.jpg'):
        files.append(os.path.join(root, filename))
    if(len(files) - size > 0) :
      print root + ": " + str(len(files) - size) + " (" + str(len(files)) + ")"
      size = len(files)

  #Show them in random order
  print "Shuffle"
  random.shuffle(files)

  pygame.font.init()
  fontPath = pygame.font.match_font(u'liberationsans')
  print fontPath
  smallfont = pygame.font.Font(fontPath, 20)
  mediumfont = pygame.font.Font(fontPath, 30)
  largefont = pygame.font.Font(fontPath, 60)

  imagenumber = 0
  for filename in files:
    imagenumber += 1

    picture = pygame.image.load(filename)
    pygame.display.set_mode((max_x,max_y), pygame.NOFRAME)
    main_surface = pygame.display.get_surface()
    imagepos = picture.get_rect()
    imagepos.centerx = main_surface.get_rect().centerx
    imagepos.centery = main_surface.get_rect().centery
    main_surface.blit(picture, imagepos)

    #Get year and month from the path
    tmptext = filename[len(dir):]
    p = re.compile('\w+')
    m = p.findall(tmptext)
    year = m[0]
    month = m[1]
    tmptext = filename[len(dir) + len(year) + len(month) + 2:]
    p = re.compile('.+\/')
    m = p.findall(tmptext)
    album = m[0]
    album = album[0:len(album)-1]

    #Display some image info
    displayText = year + "-" + month
    text = largefont.render(displayText, 1, (255, 255, 255))
    main_surface.blit(text, (0,0))
    text = mediumfont.render(album.decode('utf-8'), 1, (255, 255, 255))
    textpos = text.get_rect()
    main_surface.blit(text, (main_surface.get_rect().width - textpos.width, 0))

    #Display image number
    text = smallfont.render(str(imagenumber) + "/" + str(len(files)), 1, (255, 255, 255))
    textpos = text.get_rect()
    main_surface.blit(text, (main_surface.get_rect().width - textpos.width, main_surface.get_rect().height - textpos.height))
  
    pygame.display.flip()
    #Show for 10 seconds
    pygame.time.delay(10000)
