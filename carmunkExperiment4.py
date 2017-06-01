import random
import math
import numpy as np

import pygame
from pygame.color import THECOLORS

import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import draw
from flat_game import sonarState

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
        # Create the car.
        self.create_car(10, 350, 0.0)
        self.stateList = []

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


    def create_car(self, x, y, r):
        inertia = pymunk.moment_for_circle(1, 0, 4, (0, 0))
        self.car_body = pymunk.Body(1, inertia)
        self.car_body.position = x, y
        #self.car_shape = pymunk.Circle(self.car_body, 6)
        carSize = ( 10.0 , 5.0 )
        self.car_shape = pymunk.Poly.create_box(self.car_body, carSize)
        self.car_shape.color = THECOLORS["blue"]
        self.car_shape.elasticity = 1.0
        self.car_body.angle = r
        driving_direction = Vec2d(1, 0).rotated(self.car_body.angle)
        self.car_body.apply_impulse(driving_direction)
        self.space.add(self.car_body, self.car_shape)


    def frame_step(self, action):
        #create state list
        #check if state exists already
        stateId = self.check_State_Exists()
        if(stateId == -1):
            state = sonarState.state(self.car_body.position)
            self.stateList.append(state)
        else:
            state = self.stateList[stateId]

        if action == 0:  # Turn Left.
            self.car_body.angle -= .2
        elif action == 1: # Contiue Straight
            self.car_body.angle -= 0
        elif action == 2:  # Turn Right.
            self.car_body.angle += .2

        driving_direction = Vec2d(1, 0).rotated(self.car_body.angle)
        self.car_body.velocity = 1 * driving_direction

        # Get the current location and the readings there.
        x, y = self.car_body.position
        readings = self.get_sonar_readings(x, y, self.car_body.angle)

        # Set the reward.
        if self.car_is_crashed(readings):
            self.crashed = True
            reward = -500.00
            self.recover_from_crash(driving_direction)

        elif self.check_is_finish_line():
            reward = 1.0
        else:
            reward = -0.1
        
        self.num_steps += 1

        # Update the screen and stuff.
        screen.fill(THECOLORS["black"])
        draw(screen, self.space)
        self.space.step(1./10)
        if draw_screen:
             pygame.display.flip()
        clock.tick()
        
        return reward, state

    def check_State_Exists(self):
        for i in range(len(self.stateList)):
            if(self.stateList[i].pos == self.car_body.position):
                return i
        return -1


    def car_is_crashed(self, readings):
        if readings[0] == 1 or readings[1] == 1 or readings[2] == 1:
            return True
        else:
            return False

    def recover_from_crash(self, driving_direction):
        """
        We hit something, so recover.
        """
        while self.crashed:
            # Go backwards.
            #self.car_body.velocity = -10 * driving_direction

            # reset to start position
            self.car_body.position = 10, 350
            self.car_body.angle = 0.0
            self.crashed = False

            screen.fill(THECOLORS["red"])  # Red is scary!
            draw(screen, self.space)
            self.space.step(1./10)
            if draw_screen:
                 pygame.display.flip()
            clock.tick()

    def sum_readings(self, readings):
        """Sum the number of non-zero readings."""
        tot = 0
        for i in readings:
            tot += i
        return tot

    def get_sonar_readings(self, x, y, angle):
        readings = []
        """
        Instead of using a grid of boolean(ish) sensors, sonar readings
        simply return N "distance" readings, one for each sonar
        we're simulating. The distance is a count of the first non-zero
        reading starting at the object. For instance, if the fifth sensor
        in a sonar "arm" is non-zero, then that arm returns a distance of 5.
        """
        # Make our arms.
        arm_left = self.make_sonar_arm(x, y)
        arm_middle = arm_left
        arm_right = arm_left

        # Rotate them and get readings.
        readings.append(self.get_arm_distance(arm_left, x, y, angle, 0.75))
        readings.append(self.get_arm_distance(arm_middle, x, y, angle, 0))
        readings.append(self.get_arm_distance(arm_right, x, y, angle, -0.75))

        if show_sensors:
            pygame.display.update()

        return readings

    def get_arm_distance(self, arm, x, y, angle, offset):
        # Used to count the distance.
        i = 0

        # Look at each point and see if we've hit something.
        for point in arm:
            i += 1

            # Move the point to the right spot.
            rotated_p = self.get_rotated_point(
                x, y, point[0], point[1], angle + offset
            )

            # Check if we've hit something. Return the current i (distance)
            # if we did.
            if rotated_p[0] <= 0 or rotated_p[1] <= 0 \
                    or rotated_p[0] >= width or rotated_p[1] >= height:
                return i  # Sensor is off the screen.
            else:
                obs = screen.get_at(rotated_p)
                if self.get_track_or_not(obs) != 0:
                    return i

            if show_sensors:
                pygame.draw.circle(screen, (255, 255, 255), (rotated_p), 2)

        # Return the distance for the arm.
        return i

    def make_sonar_arm(self, x, y):
        spread = 10  # Default spread.
        distance = 2  # Gap before first sensor.
        arm_points = []
        # Make an arm. We build it flat because we'll rotate it about the
        # center later.
        for i in range(1, 40):
            arm_points.append((distance + x + (spread * i), y))

        return arm_points

    def get_rotated_point(self, x_1, y_1, x_2, y_2, radians):
        # Rotate x_2, y_2 around x_1, y_1 by angle.
        x_change = (x_2 - x_1) * math.cos(radians) + \
            (y_2 - y_1) * math.sin(radians)
        y_change = (y_1 - y_2) * math.cos(radians) - \
            (x_1 - x_2) * math.sin(radians)
        new_x = x_change + x_1
        new_y = height - (y_change + y_1)
        return int(new_x), int(new_y)

    def get_track_or_not(self, reading):
        if reading == THECOLORS['black']:
            return 0
        else:
            return 1

    def check_is_finish_line(self):
        x, y = self.car_body.position
        if(x >= 800):
           return True
        else:
           return False

if __name__ == "__main__":
    game_state = GameState()
    while True:
        game_state.frame_step((random.randint(0, 2)))
