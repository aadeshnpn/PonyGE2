import numpy as np
import math

class PotentialField:

    def __init__(self, location, null_radius, spread, strength, type='repulsor'):
        self.location = location
        self.radius = null_radius
        self.spread = spread
        self.type = type
        self.field_strength = strength
        self.infinity = 2

    def distance(self, p1, p2):
        return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def effect(self, location):
        if self.type == 'repulsor':
            d = self.distance(location, self.location)
            if d > self.radius + self.spread:
                return [0, 0]
            theta = math.atan2(self.location[1] - location[1], self.location[0] - location[0]) + np.pi/180
            #  a constant to give them some angle
            if d > self.radius:
                return [-self.field_strength*(self.spread + self.radius - d)*math.cos(theta),
                        -self.field_strength * (self.spread + self.radius - d) * math.sin(theta)]
            else:
                return [-np.sign(math.cos(theta))*self.infinity, -np.sign(math.sin(theta))*self.infinity]
        elif self.type == 'tangent':
            d = self.distance(location, self.location)
            if d > self.radius + self.spread:
                return [0, 0]
            theta = math.atan2(self.location[1] - location[1], self.location[0] - location[0]) + np.pi/2*0.95
            #  the constant term on the end gives the tangent angle minus a little to push outward as well
            if d > self.radius + 1:
                return [-self.field_strength * (self.spread + self.radius - d) * math.cos(theta),
                        -self.field_strength * (self.spread + self.radius - d) * math.sin(theta)]
            else:
                return [-np.sign(math.cos(theta)) * self.infinity, -np.sign(math.sin(theta)) * self.infinity]