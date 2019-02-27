import numpy as np
from numpy.random import random_sample as rand
from astropy import units as u
from astropy.coordinates import SkyCoord

class Cone:
    """
    """
    
    def __init__(self):
        """
        Not intended to be instantiated.
        """
        pass
    
    @staticmethod
    def random_skycoord():
        """
        """
        ra_rad = (2 * np.pi * rand()) * u.rad
        dec_rad = np.arcsin(2. * (rand() - 0.5)) * u.rad
        
        skycoord = SkyCoord(ra_rad, dec_rad)
        return skycoord
    
    @staticmethod
    def random_cone(min_radius, max_radius):
        """
        """
        if not (0 <= min_radius < max_radius):
            raise ValueError('min-radius must be in the range [0,max_radius).')
        skycoord = Cone.random_skycoord()
        radius = (max_radius - min_radius) * rand() + min_radius
        return (skycoord, radius)
    
    @staticmethod
    def generate_random(num_points, min_radius, max_radius):
        if not (0 <= min_radius < max_radius):
            raise ValueError('min-radius must be in the range [0,max_radius).')
        if num_point <= 0:
            raise ValueError('num_point must be a positive number.')  
        
        for i in range(num_points):
            cone = Cone.random_cone(min_radius, max_radius)
            yield cone
        
        

    
if __name__ == '__main__':
    x = """
    for i in range(1, 50):
        cone = Cone.random_cone(0.5, 0.6)
        print (cone)
"""
    for cone in Cone.generate_random(5, 0.1, 1.2):
        print(cone)