import random
import sys
import pygame as pg
from pygame.locals import *

import SquiggleClass as sc



pg.init()
screen = pg.display.set_mode([1920, 960])


        
tree = sc.SquiggleEvTree(screen, 240,240)


opt1 = sc.Squiggle(screen, 720,240)
opt1.randomize()
opt2 = sc.Squiggle(screen, 240,720)
opt2.randomize()
opt3 = sc.Squiggle(screen, 720,720)
opt3.randomize()

for index in range(0):
    print(index)

while True:
    for ev in pg.event.get():
        if ev.type == QUIT:
            pg.quit()
            sys.exit()
            
        if ev.type == MOUSEBUTTONUP:
            if ev.pos[0] > 480 and ev.pos[0] < 960 and ev.pos[1] > 0 and ev.pos[1] < 480:
                tree.active.loadData(opt1.dataLength,opt1.dataAngle,opt1.dataWeights)
                opt2.loadData(opt1.dataLength,opt1.dataAngle,opt1.dataWeights)
                opt2.randomize()
                opt3.loadData(opt1.dataLength,opt1.dataAngle,opt1.dataWeights)
                opt3.randomize()
            
            elif ev.pos[0] > 0 and ev.pos[0] < 480 and ev.pos[1] > 480 and ev.pos[1] < 960:
                tree.active.loadData(opt2.dataLength,opt2.dataAngle,opt2.dataWeights)
                opt1.loadData(opt2.dataLength,opt2.dataAngle,opt2.dataWeights)
                opt1.randomize()
                opt3.loadData(opt2.dataLength,opt2.dataAngle,opt2.dataWeights)
                opt3.randomize()
            
            elif ev.pos[0] > 480 and ev.pos[0] < 960 and ev.pos[1] > 480 and ev.pos[1] < 960:
                tree.active.loadData(opt3.dataLength,opt3.dataAngle,opt3.dataWeights)
                opt1.loadData(opt3.dataLength,opt3.dataAngle,opt3.dataWeights)
                opt1.randomize()
                opt2.loadData(opt3.dataLength,opt3.dataAngle,opt3.dataWeights)
                opt2.randomize()
            else:
                tree.changeActiveToPos(ev.pos[0],ev.pos[1])
                opt1.loadData(tree.active.dataLength,tree.active.dataAngle,tree.active.dataWeights)
                opt1.randomize()
                opt2.loadData(tree.active.dataLength,tree.active.dataAngle,tree.active.dataWeights)
                opt2.randomize()
                opt3.loadData(tree.active.dataLength,tree.active.dataAngle,tree.active.dataWeights)
                opt3.randomize()

        if ev.type == KEYUP:
            if ev.key == K_SPACE:
                tree.branch()
            if ev.key == K_TAB:
                tree = sc.SquiggleEvTree(screen, 240,240)

                opt1 = sc.Squiggle(screen, 720,240)
                opt1.randomize()
                opt2 = sc.Squiggle(screen, 240,720)
                opt2.randomize()
                opt3 = sc.Squiggle(screen, 720,720)
                opt3.randomize()
            if ev.key == K_BACKSPACE:
                tree.deleteActive()

                opt1.loadData(tree.active.dataLength,tree.active.dataAngle,tree.active.dataWeights)
                opt1.randomize()
                opt2.loadData(tree.active.dataLength,tree.active.dataAngle,tree.active.dataWeights)
                opt2.randomize()
                opt3.loadData(tree.active.dataLength,tree.active.dataAngle,tree.active.dataWeights)
                opt3.randomize()
            #elif ev.key == K_5:
            #    current.loadFile("Saves/test.sqg")
            #elif ev.key == K_ESCAPE:
            #    pg.quit()
                
    
    screen.fill((255,255,255))
    
    pg.draw.rect(screen, (255,200,200), (0,480, 480,480), 0)
    pg.draw.rect(screen, (200,255,200), (480,480, 480,480), 0)
    pg.draw.rect(screen, (200,200,255), (480,0, 480,480), 0)
    
    tree.active.draw()
    
    opt1.draw()
    opt2.draw()
    opt3.draw()
    for i in range(tree.depth):
        layer = tree.findLayer(i)
        for j in range(len(layer)):
            layer[j].draw(960+(960/(len(layer)+1)*(j+1)), 960/(tree.depth+1)*(i+1))
    for i in range(tree.depth):
        layer = tree.findLayer(i)
        for j in range(len(layer)):
            for target in layer[j].children:
                pg.draw.line(screen, (0,0,0), (layer[j].x, layer[j].getBounds()[1]),(target.x, target.getBounds()[3]), 2)

    pg.draw.rect(screen, (0,0,0), tree.findFromPath(tree.activePath).getRect(), 2)

    pg.display.flip()
