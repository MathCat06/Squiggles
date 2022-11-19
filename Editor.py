import random
import sys
import pygame as pg
from pygame.locals import *

import SquiggleClass as sc



pg.init()
screen = pg.display.set_mode([640, 480])


        


current = sc.Squiggle(screen, 320,120)

opt1 = sc.Squiggle(screen, 106,360)
opt1.randomize()
opt2 = sc.Squiggle(screen, 320,360)
opt2.randomize()
opt3 = sc.Squiggle(screen, 532,360)
opt3.randomize()

while True:
    for ev in pg.event.get():
        if ev.type == QUIT:
            pg.quit()
            sys.exit()
            
        if ev.type == KEYUP:
            if ev.key == K_1:
                current.loadData(opt1.dataLength,opt1.dataAngle,opt1.dataWeights)
                opt2.loadData(opt1.dataLength,opt1.dataAngle,opt1.dataWeights)
                opt2.randomize()
                opt3.loadData(opt1.dataLength,opt1.dataAngle,opt1.dataWeights)
                opt3.randomize()
            
            elif ev.key == K_2:
                current.loadData(opt2.dataLength,opt2.dataAngle,opt2.dataWeights)
                opt1.loadData(opt2.dataLength,opt2.dataAngle,opt2.dataWeights)
                opt1.randomize()
                opt3.loadData(opt2.dataLength,opt2.dataAngle,opt2.dataWeights)
                opt3.randomize()
            
            elif ev.key == K_3:
                current.loadData(opt3.dataLength,opt3.dataAngle,opt3.dataWeights)
                opt1.loadData(opt3.dataLength,opt3.dataAngle,opt3.dataWeights)
                opt1.randomize()
                opt2.loadData(opt3.dataLength,opt3.dataAngle,opt3.dataWeights)
                opt2.randomize()
                
            elif ev.key == K_4:
                current.saveFile("Saves/test.sqg")
            elif ev.key == K_5:
                current.loadFile("Saves/test.sqg")
            elif ev.key == K_ESCAPE:
                pg.quit()
                
    
    screen.fill((255,255,255))
    
    pg.draw.rect(screen, (255,220,220), (0, 240, 213,240), 0)
    pg.draw.rect(screen, (220,255,220), (213, 240, 213,240), 0)
    pg.draw.rect(screen, (220,220,255), (426, 240, 214,240), 0)
    
    current.draw()
    
    opt1.draw()
    opt2.draw()
    opt3.draw()
    
    
    
    pg.display.flip()
