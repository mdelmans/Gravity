'''
Created on Oct 5, 2012
Author: Mihails Delmans
Description:
Creates N particles with random masses densities and positions; and simulates
physical interaction between them. Color represents density of the particle.
'''

from __future__ import division
import pygame
import sys
from newton import *
from random import random,randint,seed, uniform
import argparse

seed();

class Simulation():
	def __init__(self, displayW = 1200, displayH = 700, nParticles = 40, drawPath = True, fps = 30):
		self.displayW = displayW
		self.displayH = displayH
		self.nParticles = nParticles
		self.drawPath = drawPath
		self.fps = fps

		self.clock = pygame.time.Clock()
		
		pygame.init()
		self.DISPLAYSURF = pygame.display.set_mode((self.displayW, self.displayH))
		pygame.display.set_caption("Gravity")

		self.reset()

	def reset(self):
		self.particle = []
		for i in range(self.nParticles):
			self.particle.append(Particle( randint(27,300), random(), (randint(200, self.displayW-200), randint(200, self.displayH-200)) )  )

	def run(self):
		while True:
			if len(self.particle) < 2:
				self.reset()
			
			self.DISPLAYSURF.fill(DBLUE)
			
			for p in self.particle:
				p.draw(self.DISPLAYSURF, drawPath=self.drawPath);
			
			for pi in self.particle:
				if pi.pos[0] < 0 or pi.pos[0] > self.displayW or pi.pos[1] < 0 or pi.pos[1] > self.displayH:
					self.particle.pop(self.particle.index(pi))
					break

				Ftotal = array([0,0])
				for pj in self.particle:
					if pi != pj:
						Ftotal = Ftotal + force(pi,pj)
						if distance(pi,pj)*1.5 < pi.radius + pj.radius:
							pj.velocity  = (pi.velocity*pi.mass + pj.velocity*pj.mass) / (pi.mass + pj.mass)
							
							
							pj.density = (pi.density*(pi.radius**3) + pj.density*(pj.radius**3)) / (pj.radius**3 + pi.radius**3)
							pj.mass = pj.mass + pi.mass
							self.particle.pop(self.particle.index(pi))
							break
				
				pi.path.append(pi.pos)

				pi.pos = pi.pos + pi.velocity + Ftotal / (2 * pi.mass)
				pi.velocity = pi.velocity + Ftotal / pi.mass
			
			for event in pygame.event.get():
				if event.type ==QUIT:
					pygame.quit()
					sys.exit
			
			pygame.display.update()
			self.clock.tick(self.fps)

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Gravity simulation')
	parser.add_argument( '-dW', type = int, default = 1000, help = 'Display width' )
	parser.add_argument( '-dH', type = int, default = 700, help = 'Display height' )
	parser.add_argument( '-N', type = int, default = 40, help = 'Number of particles' )
	parser.add_argument( '--path', action = 'store_true', help = 'Draw path')

	args = parser.parse_args()

	simulation = Simulation(args.dW, args.dH, args.N, args.path)
	simulation.run()

