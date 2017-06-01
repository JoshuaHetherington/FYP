import random
import math
import numpy as np

import pygame
from pygame.color import THECOLORS

import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import draw
from flat_game import cell2

# PyGame init
width = 1000
height = 700
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Turn off alpha since we don't use it.
screen.set_alpha(None)

# Showing sensors and redrawing slows things down.
show_sensors = True
draw_screen = True


class GameState:
    def __init__(self):
        # Global-ish.
        self.crashed = False

        # Physics stuff.
        self.space = pymunk.Space()
        self.space.gravity = pymunk.Vec2d(0., 0.)

        # Record steps.
        self.num_steps = 0

        # Create walls.
        static = [
            pymunk.Segment(
                self.space.static_body,
                (0, 1), (0, height), 1),
            pymunk.Segment(
                self.space.static_body,
                (1, height), (width, height), 1),
            pymunk.Segment(
                self.space.static_body,
                (width-1, height), (width-1, 1), 1),
            pymunk.Segment(
                self.space.static_body,
                (1, 1), (width, 1), 1)
        ]
        for s in static:
            s.friction = 1.
            s.group = 1
            s.collision_type = 1
            s.color = THECOLORS['red']
        self.space.add(static)
        self.create_track()
        x = 0
        y = 0
        self.cellList = self.create_cells()
        startPos = self.getStart()
        x = startPos.x
        y = startPos.y
        # Create the car.
        self.create_car(x, y, 0.5)

    def create_track(self):
        height = 310
        height2nd = 390
        static2nd = [
            pymunk.Segment(
                self.space.static_body,
                (0, height), (width, height), 3),
            pymunk.Segment(
                self.space.static_body,
                (0, height2nd), (width, height2nd), 3)
        ]
        for s in static2nd:
            s.friction = 1.
            s.group = 1
            s.collision_type = 1
            s.color = THECOLORS['yellow']
        self.space.add(static2nd)

    def create_cells(self):
        #create cells 4 x 10 (20 x 100) 
        start = False
        end = False
        current = False
        rows = 4
        columns = 10
        y = 310
        cellList = []
        #while a < rows:
        for i in range(rows):
             #statements
             cellTempList = []
             x = 0
             #while b < columns:
             for j in range(columns):
                  #statements
                  #firstX = 0 firstY = 310      
                  centrePos = self.findCentre(x, y)
                  #cell(centrePos, current, start, end)
                  if(j == 9):
                          end = True
                  tempCell = cell2.cell2(centrePos, current, start, end)
                  cellTempList.append(tempCell)
                  x =  x + 100
             y = y + 20
             end = False
             cellList.append(cellTempList)

        cellList[2][0].start = True
        cellList[2][0].current = True
        return cellList
        
    def getStart(self):
        for r in range(4):
             for c in range(10):
                  if (self.cellList[r][c].start):
                       centrePos = self.cellList[r][c].centrePos
        return centrePos
        
    def findCentre(self, x1, y1):
        x2 = x1 + 100
        y2 = y1 + 20
        centreX = (x2 + x1) / 2
        centreY = (y2 + y1) / 2
        centrePos = Vec2d(centreX, centreY)
        return centrePos

    def create_car(self, x, y, r):
        inertia = pymunk.moment_for_circle(1, 0, 4, (0, 0))
        self.car_body = pymunk.Body(1, inertia)
        self.car_body.position = x, y
        self.car_shape = pymunk.Circle(self.car_body, 6)
        #carSize = ( 10.0 , 5.0 )
        #self.car_shape = pymunk.Poly.create_box(self.car_body, carSize)
        self.car_shape.color = THECOLORS["blue"]
        self.car_shape.elasticity = 1.0
        self.car_body.angle = r
        driving_direction = Vec2d(1, 0).rotated(self.car_body.angle)
        self.car_body.apply_impulse(driving_direction)
        self.space.add(self.car_body, self.car_shape)

    def check_For_Crash(self, row, column):
        if(row < 0 or row > 3):
             #print("Crash Row")
             return True
        elif(column < 0 or column > 9):
             #print("Crash Column")
             return True
        else:
             return False

    def frame_step(self, action):
        crashed = False
        for i in range(4):
                 for j in range(10):
                      if(self.cellList[i][j].current):
                           row = i
                           column = j

        if action == 0:  # Turn UP.
            crashed = self.check_For_Crash(row - 1, column)
            if (crashed == False):
                 row = row - 1
                 self.cellList[row + 1][column].current = False
                 self.cellList[row][column].current = True
                 pos = self.cellList[row][column].centrePos
                 self.car_body.position = pos.x, pos.y

        elif action == 1: # Move Right
            crashed = self.check_For_Crash(row, column + 1)
            if (crashed == False):
                 column = column + 1
                 self.cellList[row][column - 1].current = False
                 self.cellList[row][column].current = True
                 pos = self.cellList[row][column].centrePos
                 self.car_body.position = pos.x, pos.y

        elif action == 2:  # Turn DOWN.
            crashed = self.check_For_Crash(row + 1, column)
            if (crashed == False):
                 row = row + 1
                 self.cellList[row - 1][column].current = False
                 self.cellList[row][column].current = True
                 pos = self.cellList[row][column].centrePos
                 self.car_body.position = pos.x, pos.y

        elif action == 3: # Turn Left
            crashed = self.check_For_Crash(row, column - 1)
            if (crashed == False):
                 column = column - 1
                 self.cellList[row][column + 1].current = False
                 self.cellList[row][column].current = True
                 pos = self.cellList[row][column].centrePos
                 self.car_body.position = pos.x, pos.y

        self.num_steps += 1
        if(crashed):
            self.cellList[row][column].current = False
            self.cellList[2][0].current = True
            crashed = False
            reward = -50.0
            startPos = self.getStart()
            self.car_body.position = startPos.x, startPos.y

        else:
            currentCell = self.cellList[row][column]
            if (currentCell.end):
                 reward = 1.0
                 startPos = self.getStart()
                 self.car_body.position = startPos.x, startPos.y
            else:
                 reward = -0.1
        
        #comment the below out to speed up computation, or un-comment to use display
        screen.fill(THECOLORS["grey"])
        draw(screen, self.space)
        self.space.step(1./10)
        if draw_screen:
             pygame.display.flip()
        clock.tick()
        
        return reward

    def printMove(self, x, y, r, c):
        print("After Move - X: %d\t Y: %d\t Row: %d\t Column: %d" %
              (x, y, r, c))

if __name__ == "__main__":
    game_state = GameState()
    while True:
        game_state.frame_step((random.randint(0, 2)))
