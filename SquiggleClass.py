import numpy as np
import random
import pygame as pg
from pygame.locals import *
from math import sin, cos, radians, pi

def point_pos(x0, y0, d, theta): # Use trig to find point from point, angle and distance
    theta_rad = pi/2 - radians(theta)
    return x0 + d*cos(theta_rad), y0 + d*sin(theta_rad)


class Squiggle:
    def __init__(self, sc, x, y):
        self.screen = sc # Pygame Screen to draw to
        self.x = x # Coordinates of Squiggle on screen
        self.y = y
        self.padding = 20 # Padding around squiggle for outlines and clicking
        self.angle = 0 # Rotation to draw at
        self.dataLength = np.array([15]) # Line length data
        self.dataAngle = np.array([1]) # Line angle data
        self.dataWeights = np.array([.33]) # Line Weight data
        self.children = [] # List of squiggle children
        
    def draw(self, x = None, y = None): # draw squiggle at last coordinates, or given coordinates
        currentPos = np.array([0,0]) # keep track of positions and angles
        currentAngle = np.array([self.angle])
        
        for index in range(len(self.dataLength)): # loop for every line
        
            if x != None: # change x and y position, if needed
                self.x = x
            if y != None:
                self.y = y

            # Draw mirrored lines from previous position to a new posision determined by length and angle data
            pg.draw.line(self.screen, (0,0,0), ( currentPos[-2]+self.x, currentPos[-1]+self.y), point_pos( currentPos[-2]+self.x, currentPos[-1]+self.y, self.dataLength[index], self.dataAngle[index] + currentAngle[-1] ),2)
            pg.draw.line(self.screen, (0,0,0), ( -currentPos[-2]+self.x, currentPos[-1]+self.y), point_pos( -currentPos[-2]+self.x, currentPos[-1]+self.y, self.dataLength[index], -self.dataAngle[index] - currentAngle[-1] ),2)
            
            # If self.dataAngle[index]%2 == 0: # add new point to list of points / option for: only if dataAngle is even
            currentPos = np.append(currentPos,currentPos[-2])
            currentPos = np.append(currentPos,currentPos[-2])
            currentAngle = np.append(currentAngle,currentAngle[-1])
            
            
            # Change new point to correct position
            currentPos[-2] = currentPos[-2] + self.dataLength[index]*cos(pi/2 - radians(self.dataAngle[index]+currentAngle[-1]))
            currentPos[-1] = currentPos[-1] + self.dataLength[index]*sin(pi/2 - radians(self.dataAngle[index]+currentAngle[-1]))
            currentAngle[-1] += self.dataAngle[index]
        
            
            if self.dataAngle[index]%4 == 0: # move back points if angle is divisible by 4
                for rep in range(self.dataLength[index]%7): # move 1-7 back, depending on length of data
                    if len(currentAngle) > 1: # don't delete origin point
                        currentPos = np.delete(currentPos, -1) # delete point in stack, branching from earlier point
                        currentPos = np.delete(currentPos, -1)
                        currentAngle = np.delete(currentAngle, -1)
                        
    
    def randomize(self): # modify data randomly
        
        for index in range(len(self.dataWeights)): # modify each point
            if random.random() > self.dataWeights[index]: # only modify some, based on weight. higher weight = less modification
                self.dataLength[index] += round(random.randint(-25,25)*self.dataWeights[index]) # randomize length, less if higher weight
                if self.dataLength[index] < 1: # length can't be less then 1
                    self.dataLength[index] = 1
                
                self.dataAngle[index] += round(random.randint(-90,90)*self.dataWeights[index]) # randomize angle, less if higher weight
                
                self.dataWeights[index] *= .9 # weight is less sure
            else:
                self.dataWeights[index] += (1-self.dataWeights[index])*.75 # if same, the weight is more sure
        
        
        if random.random() > .5: # 50% chance to add extra line, with random length and angle
            self.dataLength = np.append(self.dataLength, random.randint(5,30))
            self.dataAngle = np.append(self.dataAngle, random.randint(-90,90))
            self.dataWeights = np.append(self.dataWeights, .33)
  
    def loadData(self,lengths,angles,weights): # load drawing data from lists
        self.dataLength = np.array(lengths)
        self.dataAngle = np.array(angles)
        self.dataWeights = np.array(weights)

    def loadSquiggle(self,squiggle): # load drawing data and children from squiggle
        self.dataLength = squiggle.dataLength
        self.dataAngle = squiggle.dataAngle
        self.dataWeights = squiggle.dataWeights
        self.children = squiggle.children
        
    def saveFile(self, path): # --Not Complete-- save data to a .sqg file


        ### Format:
        ##
        ##SQG
        ##len1_len2_len3_
        ##ang1_ang2_ang3_
        ##wgt1_wgt2_wgt3_
        
        file  = open(path, "w")
        file.write("")
        file.close()
        
        file = open(path, "a")
        file.write("SQG\n")
        
        for index in range(len(self.dataLength)):
            file.write(str(self.dataLength[index]))
            file.write("_")
        
        file.write("\n")
        
        for index in range(len(self.dataAngle)):
            file.write(str(self.dataAngle[index]))
            file.write("_")
        
        file.write("\n")
        
        for index in range(len(self.dataWeights)):
            file.write(str(self.dataWeights[index]))
            file.write("_")
            
        
        file.close()
    
    def loadFile(self, path): # --Not Complete-- load data from a .sqg file

        ### Format same as above
        
        file = open(path, "r")
        
        line = file.readline()
        
        if line == "SQG":
            line = file.readline()
            items = line.count("_")
            dataLength = np.array([])
            for index in range(items):
                dataLength = append(dataLength, int(line.split("_")[index]))
                
            line = file.readline()
            items = line.count("_")
            dataAngle = np.array([])
            for index in range(items):
                dataAngle = append(dataAngle, int(line.split("_")[index]))
            
            line = file.readline()
            items = line.count("_")
            dataWeights = np.array([])
            for index in range(items):
                dataWeights = append(dataWeights, int(line.split("_")[index]))
                    
        file.close()

    def getBounds(self): # Get x and y coords for top left and bottom right corners of bounding box, with padding added

        output = [0,0,0,0] # set up coords
        currentPos = np.array([0,0]) # go through drawing sequence - see draw() above
        currentAngle = np.array([self.angle])
        
        for index in range(len(self.dataLength)):
            
            if self.dataAngle[index]%2 == 0:
                currentPos = np.append(currentPos,currentPos[-2])
                currentPos = np.append(currentPos,currentPos[-2])
                currentAngle = np.append(currentAngle,currentAngle[-1])
            
            
        
            currentPos[-2] = currentPos[-2] + self.dataLength[index]*cos(pi/2 - radians(self.dataAngle[index]+currentAngle[-1]))
        
            currentPos[-1] = currentPos[-1] + self.dataLength[index]*sin(pi/2 - radians(self.dataAngle[index]+currentAngle[-1]))
        
            currentAngle[-1] += self.dataAngle[index]

            
            if abs(currentPos[-2]) > output[2]: # modify data if point exceeds current bounds
                output[0] = -abs(currentPos[-2])
                output[2] = abs(currentPos[-2])

            if currentPos[-1] > output[1]:
                output[1] = currentPos[-1]

            if currentPos[-1] < output[3]:
                output[3] = currentPos[-1]

            
            if self.dataAngle[index]%4 == 0:
                for rep in range(self.dataLength[index]%7):
                    if len(currentAngle) > 1:
                        currentPos = np.delete(currentPos, -1)
                        currentPos = np.delete(currentPos, -1)
                        currentAngle = np.delete(currentAngle, -1)

        output[0] += self.x-self.padding # add padding after bounds established
        output[2] += self.x+self.padding
        output[1] += self.y+self.padding
        output[3] += self.y-self.padding
        
        return output # output coords

    def getRect(self): # output bounds in rect format, with top left corner, width, and height
        output = self.getBounds() # get bound coords

        output[2] = output[2] - output[0] # change second point to width and height
        output[3] = output[3] - output[1]
        
        return output # output rect


class SquiggleEvTree:
    def __init__(self, sc, x, y):
        self.base = Squiggle(sc, x, y) # create basic squiggle
        self.active = Squiggle(sc, x, y) # active is the same as base
        self.activePath = [] # keep track of where the active squiggle is located
        self.depth = 1 # keep track of deepest squiggle
        
    def changeActive(self, path): # change active squiggle based on path
        selected = self.base
        for index in path: # loop through path, moving into indicated child
            selected = selected.children[index]
        self.active.loadSquiggle(selected) # change active and active path
        self.activePath = path

    def changeActiveToPos(self, x, y): # change active based on coordinate position
        layer = 0 # start looking in layer 0
        while True: # Loop through layers
            
            targets = self.findLayer(layer) # find all squiggles in layer

            if len(targets) == 0: # if empty, end
                return
            else:
                for target in targets: # loop through squiggles in layer
                    bounds = target.getBounds() # find target bounds
                    if bounds[0] < x and x < bounds[2] and bounds[3] < y and y < bounds[1]: # change to active if coords are within bounds
                        self.active.loadSquiggle(target)
                        self.activePath = self.findPath(target,[])
                        return
            layer += 1 # next layer

    def deleteActive(self): # delete active squiggle, along with all children
        if len(self.activePath) > 0: # don't delete base
            child = self.activePath.pop(-1) # move active path back 1, saving the deleted value
            self.findFromPath(self.activePath).children.pop(child) # delete active
            self.changeActive(self.activePath) # change active to match active path

        if len(self.findLayer(self.depth-1)) == 0: # change depth if deleted was last in its layer
            self.depth -= 1
            
    def branch(self): # make modified active a child of its unmodified version
        selected = self.base
        for index in self.activePath: # find active in tree
            selected = selected.children[index]
        selected.children.append(Squiggle(self.active.screen, self.active.x, self.active.y)) # add child
        selected.children[-1].loadData(self.active.dataLength,self.active.dataAngle,self.active.dataWeights) # load child
        self.activePath.append(len(selected.children)-1) # modify path
        if len(self.activePath)+1 > self.depth: # change depth, if necessary
            self.depth += 1

    def findFromPath(self, path): # return the squiggle at a path location
        selected = self.base
        for index in range(len(path)): # loop through path
            try:
                selected = selected.children[path[index]]
            except:
                return index # if it fails, return the depth of the failure
        return selected # if it works, return the squiggle

    def findPath(self, squiggle, path): # return the path of a given squiggle
        current = self.findFromPath(path) # path to look in first

        if current == squiggle: # return if correct
            return path
        path.append(0) # otherwise, loop through children, calling this function recursively
        for index in range(len(current.children)):
            path[-1] = index
            result = self.findPath(squiggle, path)
            if result != False: # if a child finds it, return the result
                return result
        path.pop() # otherwise, move back in the path and return false
        return False

    def findLayer(self, layer): # return a list of all squiggles in a given layer
        output = []
        path = []

        if layer == 0: # special case for layer 0
            output.append(self.base)
            return output
        
        for i in range(layer): # create a path as deep as the target layer
            path.append(0)

        while path[0] < len(self.base.children): # while the path is in the tree, loop
            result = self.findFromPath(path) # try to find a squiggle at the path
            if type(result) == int: # if failed, increase the path 1 above the point of failure, resetting everything below
                for i in range(len(path)-result):
                    path[-(i+1)] = 0
                
                path[result-1] += 1
                
            else:
                output.append(result) # otherwise, add result and move on to the next path
                path[-1] += 1
        return output # once searched, return the list

        


