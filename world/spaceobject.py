"""
Space Object

The Space Object is quite literally an object in space. It is an object that
appears repeatedly, on an apparently random basis. It encompasses things such
as Planets, Stars, Moons, Asteroid Fields, etc.

Usage:

    Once the implementation details are worked out, usage be noted here.

Implementation:

    Once the implementation details are worked out, they will be noted here.

# TODO: Update this doc
"""

# from typeclasses.objects import Object
from noise import snoise3
import random


class SpaceObject(object):
    # This should inherit from `Object` before we start using it with Evennia
    # In order to run spaceobj-test.py, change it to `object`
    """
    The SpaceObject class is the parent class for the individual classes for the
    various types of objects you might find in space. It has all of the generic
    functions necessary for an object that appears scattered through space.
    """
    def __init__(self, seed, occurs=75):
        self.seed = seed
        self.occurs = occurs
        # Simplex Noise doesn't work on integers, so lets get some seeded
        # random offsets (non-integer) for x, y, and z to overcome this limitation.
        random.seed(self.seed)
        self.xoffset = random.random()
        self.yoffset = random.random()
        self.zoffset = random.random()

    def object_at_coordinates(self, coordinates):
        """
        Determines if there is an object at the specified coordinates

        Args:
            coordinates (tuple, (int, int, int)): The coordinates to check

        Returns:
            Returns a boolean. `True` if there is an object at the specified
            coordinates and `False` if there is not.
        """
        x, y, z = coordinates
        n = snoise3(x + self.xoffset, y + self.yoffset, z + self.zoffset)
        o = int(n * 100)
        return o <= self.occurs


class Star(SpaceObject):
    """
    One of the most basic space objects, the star simply exists
    """
    def __init__(self, seed=39, occurs=75):
        super(Star, self).__init__(seed=seed, occurs=occurs)


class Planet(Star):
    """
    The planet exists only where there are stars, but not in every location
    """
    def __init__(self, seed=39, star_occurs=75, occurs=75):
        super(Planet, self).__init__(seed=seed, occurs=star_occurs)
        self.occurs = occurs

    def object_at_coordinates(self, coordinates):
        if super(Planet, self).object_at_coordinates(coordinates):
            x, y, z = coordinates
            n = snoise3(x + self.xoffset, y + self.yoffset, z + self.zoffset)
            o = int(n * 100)
            return o <= self.occurs
        else:
            return False


class Moon(Planet):
    """
    The moon exists only where there is a planet, but not in every location
    """
    def __init__(self, seed=39, star_occurs=75, planet_occurs=75, occurs=30):
        super(Moon, self).__init__(seed=seed, occurs=planet_occurs)
        self.planet_occurs = planet_occurs
        self.moon_occurs = occurs

    def object_at_coordinates(self, coordinates):
        if super(Moon, self).object_at_coordinates(coordinates):
            x, y, z = coordinates
            n = snoise3(x + self.xoffset, y + self.yoffset, z + self.zoffset)
            o = int(n * 100)
            return o <= self.occurs
        else:
            return False
