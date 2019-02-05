"""
Space Ship

The ship (space) is a vehicle for space navigation.

It sounds silly to call it a "Space Ship," but we need to leave room for ocean-
    going vessels that could be added at a later time.

The ship is comprised of at least three components:
* The Bridge (room)     - The minimum interior of the vessel
* A Console (object)    - The means to control the ship
* The Hull (object)     - The exterior of the ship, as seen in Space

It is possible for a ship to have more than one Console, however it may never
    have more than one Hull or Bridge.
"""

from evennia import DefaultRoom
from typeclasses.objects import Object


class SpaceShipBridge(DefaultRoom, Object):
    """
    The Bridge is the main room of the ship. It typically contains a Console,
    although this is not always the case. The Bridge _is_ required for a
    functioning ship. Other rooms may be attached to the Bridge to create a
    larger ship.
    """
    pass


class SpaceShipConsole(Object):
    """
    The Console is the means to control the ship. There is at least one Console
    on every ship.
    """
    pass


class SpaceShipHull(Object):
    """
    The Hull is the exterior of the ship, and is what travels through space.
    """
    pass
