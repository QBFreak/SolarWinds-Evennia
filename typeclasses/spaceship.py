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
from world.space import SpaceRoom


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
    def at_object_creation(self):
        """
        Called when the object is first created
        """
        self.cmdset.add("spaceshipconsole.SSCCmdSet")

    def return_appearance(self, looker):
        """
        Called by the look command.
        """
        # Default appearance
        string = super(SpaceShipConsole, self).return_appearance(looker)

        # Error messages
        errors = False
        if not self.db.hull:
            string += "\n|rERROR:|n Console does not have a Hull specified."
            errors = True
        elif not isinstance(self.db.hull, SpaceShipHull):
            string += "\n|rERROR:|n Console has an invalid Hull specified."
            errors = True
        else:
            # No Hull errors, check Console re: Hull
            if not self.db.hull.db.console:
                string += "\n|rERROR:|n Hull does not have a Console specified."
                errors = True
            elif not isinstance(self.db.hull.db.console, SpaceShipConsole):
                string += "\n|rERROR:|n Hull has an invalid Console specified."
                errors = True
            elif self.db.hull.db.Console.db.hull != self.db.hull:
                string += "\n|rERROR:|n Hull's Console specifies a different Hull!'"
                errors = True

        if not self.db.bridge:
            string += "\n|rERROR:|n Console does not have a Bridge specified."
            errors = True
        elif not isinstance(self.db.bridge, SpaceShipBridge):
            string += "\n|rERROR:|n Console has an invalid Bridge specified."
            errors = True
        else:
            # No Bridge errors, check Console re: Bridge
            if not self.db.bridge.db.console:
                string += "\n|rERROR:|n Bridge does not have a Console specified."
                errors = True
            elif not isinstance(self.db.bridge.db.console, SpaceShipConsole):
                string += "\n|rERROR:|n Bridge has an invalid Console specified."
                errors = True
            elif self.db.bridge.db.Console.db.bridge != self.db.bridge:
                string += "\n|rERROR:|n Bridge's Console specifies a different Bridge!'"
                errors = True

        # If we had any errors, then exit here
        if errors:
            return string

        if isinstance(self.db.hull.location, SpaceRoom):
            string += "\nCoordinates: {}".format(self.db.hull.location.coordinates)
        else:
            string += "\nCoordinates: Unknown"
        # Done
        return string


class SpaceShipHull(Object):
    """
    The Hull is the exterior of the ship, and is what travels through space.
    """
    pass
