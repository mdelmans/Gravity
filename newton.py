'''
Created on Oct 4, 2012
Author: Mihails Delmans
Description:
Defines Particle class and common functions.
'''
from __future__ import division

WHITE = (255,255,255)
BLACK = (  0,  0,  0)
DBLUE = (  0,  0, 50)

import pygame
from numpy import *
from pygame.locals import *
import sys

class Particle:
    def __init__(self,mass,density,pos):
        self.mass = mass
        self.pos = pos
        self.velocity = array([0,0])
        self.density = density
        self.radius = int(round((self.mass / self.density)**(1/3)))
        self.path = []
        
        
    def draw(self, CANVAS, drawPath = False):
        self.radius = int(round(self.mass / self.density)**(1/3))
        color = int(round(255 - self.density * 255))
        pygame.draw.circle(CANVAS, (color,color,color),(int(round(self.pos[0])),int(round(self.pos[1]))), self.radius, 0)

        if drawPath:
            if len( self.path ) > 1:
                pygame.draw.aalines(CANVAS, (color, color, color), False, self.path, 1)

G = 0.5
def distance(particle1,particle2):
    return  math.sqrt((particle1.pos[0] - particle2.pos[0])**2 + (particle1.pos[1]-particle2.pos[1])**2)
        
def d_vector(origin,destination):
    return array(destination.pos) - array(origin.pos)
def force(particle1,particle2):
    return G  * particle1.mass*particle2.mass / distance(particle1, particle2)**3 * d_vector(particle1, particle2)    