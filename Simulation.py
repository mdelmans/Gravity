'''
Created on Oct 5, 2012
Author: Mihails Delmans
Description:
Creates N particles with random masses densities and positions; and simulates
physical interaction between them. Color represents density of the particle.
'''

from __future__ import division
import pygame
#from pygame.locals import *
import sys
from Newton import *
from random import random,randint,seed, uniform


seed();

display_W = 1400
display_H = 800

particle = []
def makeparticles(N=40):
    global particle
    particle = []
    for i in range(N):
        particle.append(Particle( randint(27,300), random(), (randint(200,display_W-200),randint(200,display_H-200)) )  )

fpsClock = pygame.time.Clock()
FPS = 30

pygame.init()

DISPLAYSURF = pygame.display.set_mode((display_W,display_H))
pygame.display.set_caption("Gravity")


while True:
    if len(particle) < 2 :
        makeparticles()
    DISPLAYSURF.fill(DBLUE)
    for p in particle:
        p.draw(DISPLAYSURF);
    
    for pi in particle:
        Ftotal = array([0,0])
        for pj in particle:
            if pi.pos[0] < 0 or pi.pos[0] > display_W or pi.pos[1] < 0 or pi.pos[1] > display_H:
                particle.pop(particle.index(pi))
                break
            if pi != pj:
                Ftotal = Ftotal + force(pi,pj)
                if distance(pi,pj)*1.05 < pi.radius + pj.radius:
                    pj.velocity  = (pi.velocity*pi.mass + pj.velocity*pj.mass) / (pi.mass + pj.mass)
                    
                    
                    pj.density = (pi.density*(pi.radius**3) + pj.density*(pj.radius**3)) / (pj.radius**3 + pi.radius**3)
                    pj.mass = pj.mass + pi.mass
                    particle.pop(particle.index(pi))
                    break
        
                
        
        pi.pos = pi.pos + pi.velocity + Ftotal / (2 * pi.mass)
        pi.velocity = pi.velocity + Ftotal / pi.mass
    
    for event in pygame.event.get():
        if event.type ==QUIT:
            pygame.quit()
            sys.exit
    
    pygame.display.update( )
    fpsClock.tick(FPS)