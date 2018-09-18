"""
Space Object

The Space Object is quite literally an object in space. It is an object that
appears repeatedly, on an apparently random basis. It encompasses things such
as Planets, Stars, Moons, Asteroid Fields, etc.

Usage:

    Once the implementation details are worked out, usage be noted here.

Implementation:

    Once the implementation details are worked out, they will be noted here.
"""

# from typeclasses.objects import Object
from noise import snoise3
import random


class SpaceObject(Object):
    # TODO: This should inherit from `Object` before we start using it with Evennia
    # In order to run spaceobj-test.py, change it to `object`
    """
    The SpaceObject class is the parent class for the individual classes for the
    various types of objects you might find in space. It has all of the generic
    functions necessary for an object that appears scattered through space.
    """
    def __init__(self, seed, scale=2, selection=1):
        self.seed = seed
        self.scale = scale
        self.selection = selection
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
        o = int(n * self.scale)
        return o == self.selection


class Star(SpaceObject):
    """
    One of the most basic space objects, the star simply exists
    """
    def __init__(self, seed=39, scale=2, selection=1):
        super(Star, self).__init__(seed, scale, selection)


class Planet(Star):
    """
    The planet exists only where there are stars, but not in every location
    """
    def __init__(self, seed=39, scale=2, selection=1):
        super(Planet, self).__init__(seed, scale, selection)
        self.range = 5
        self.occurs = 4

    def object_at_coordinates(self, coordinates):
        if super(Planet, self).object_at_coordinates(coordinates):
            # Because random was seeded in SpaceObject.__init__(), it's ready
            # to produce consistent results for us.
            return random.randint(0, self.range) == self.occurs
        else:
            return False


class Moon(Planet):
    """
    The moon exists only where there is a planet, but not in every location
    """
    def __init__(self, seed=39, scale=2, selection=1):
        super(Moon, self).__init__(seed, scale, selection)
        self.range = 5
        self.occurs = 3

    def object_at_coordinates(self, coordinates):
        if super(Moon, self).object_at_coordinates(coordinates):
            # Because random was seeded in SpaceObject.__init__(), it's ready
            # to produce consistent results for us.
            return random.randint(0, self.range) == self.occurs
        else:
            return False
