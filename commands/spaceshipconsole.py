"""
SpaceShipConsole Commands

These are the commands and command set for the SpaceShipConsole
"""

from evennia import CmdSet
from evennia import Command
from typeclasses.spaceship import SpaceShipHull
from world.space import SpaceRoom


class SSCCmdSet(CmdSet):
    """
    The `SSCCmdSet` contains space-ship console-specific commands like `lon` and
    `lat`, as well as other navigation and ship control commands. It is applied
    to the Console on creation.
    """
    key = "SSCCmdSet"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        self.add(CmdSSCLat())
        self.add(CmdSSCLon())
        self.add(CmdSSCStep())
        self.add(CmdSSCPort())
        self.add(CmdSSCStarboard())
        self.add(CmdSSCUp())
        self.add(CmdSSCDown())

        # TODO: Lat/Lon command adjusting for entries > 360 using `% 360`


class CmdSSCLat(Command):
    """
    Set the Latitude for the current course

    Usage:
      lat [<value>]

    View or set the latitude of the current course. Calling with no parameters
        will display the current latitude. When specifying a latitude, it must
        be in 45-degree increments.
    """

    key = "lat"
    aliases = ["latitude"]
    locks = "cmd:all()"
    help_category = "General"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):
        "Display or verify and set the latitude"
        caller = self.caller
        if not self.target:
            if not self.obj.db.lat:
                self.obj.db.lat = 0
            caller.msg("The current latitude is {}".format(self.obj.db.lat))
        else:
            if int(self.target) % 45 != 0:
                caller.msg("Latitude must be entered in increments of 45 degrees")
            else:
                self.obj.db.lat = int(self.target)
                caller.msg("The current latitude has been set to {}".format(self.obj.db.lat))


class CmdSSCLon(Command):
    """
    Set the Longitude for the current course

    Usage:
      lon [<value>]

    View or set the longitude of the current course. Calling with no parameters
        will display the current longitude. When specifying a longitude, it must
        be in 45-degree increments.
    """

    key = "lon"
    aliases = ["longitude"]
    locks = "cmd:all()"
    help_category = "General"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):
        "Display or verify and set the longitude"
        caller = self.caller
        if not self.target:
            if not self.obj.db.lon:
                self.obj.db.lon = 0
            caller.msg("The current longitude is {}".format(self.obj.db.lon))
        else:
            if int(self.target) % 45 != 0:
                caller.msg("Longitude must be entered in increments of 45 degrees")
            else:
                self.obj.db.lon = int(self.target) % 360
                caller.msg("The current longitude has been set to {}".format(self.obj.db.lon))


class CmdSSCStep(Command):
    """
    Take a step into the next system, along the ship's current course. This is a
        temporary command.

    Usage:
        step

    Temporary command to step the ship into the next system along it's current
        course.
    """

    key = "step"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):
        "Take a step towards the next system"
        caller = self.caller
        if self.target:
            caller.msg("Step does not take any parameters")
            return
        ship = self.obj.db.hull
        if not isinstance(ship, SpaceShipHull):
            caller.msg("Error locating ship!")
            return
        if not isinstance(ship.location, SpaceRoom):
            caller.msg("Cannot step ship that is not in space!")
            return
        coordinates = list(ship.location.coordinates)
        x = 0
        y = 0
        z = 0
        # Lat == 0 or Lat == 180: Ship upside down re ecliptic
        if self.obj.db.lat > 0 and self.obj.db.lat < 180:
            z = 1
        if self.obj.db.lat > 180 and self.obj.db.lat < 360:
            z = -1
        if self.obj.db.lon > 270 or self.obj.db.lon < 90:
            y = 1
        if self.obj.db.lon > 90 and self.obj.db.lon < 270:
            y = -1
        if self.obj.db.lon > 0 and self.obj.db.lon < 180:
            x = 1
        if self.obj.db.lon > 180 and self.obj.db.lon < 360:
            x = -1
        coordinates[0] += x
        coordinates[1] += y
        coordinates[2] += z
        coordinates = tuple(coordinates)
        caller.msg("The new coordinates are {}, {}, {}".format(
            coordinates[0], coordinates[1], coordinates[2]
        ))


class CmdSSCPort(Command):
    """
    Turn the ship to port, 45 degrees

    Usage:
        port

    This command may be temporary. It adjusts the ships longitude towards port
        by 45 degrees.
    """

    key = "port"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):
        "Turn ship to port"
        self.obj.db.lon = (self.obj.db.lon - 45 + 360) % 360
        self.caller.msg("The ship is now oriented to {} longitude.".format(self.obj.db.lon))


class CmdSSCStarboard(Command):
    """
    Turn the ship to starboard, 45 degrees

    Usage:
        starboard

    This command may be temporary. It adjusts the ships longitude towards
        starboard by 45 degrees.
    """

    key = "starboard"
    aliases = ["star"]
    locks = "cmd:all()"
    help_category = "General"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):
        "Turn ship to starboard"
        self.obj.db.lon = (self.obj.db.lon + 45) % 360
        self.caller.msg("The ship is now oriented to {} longitude.".format(self.obj.db.lon))


class CmdSSCUp(Command):
    """
    Pitch the ship to up, 45 degrees

    Usage:
        up

    This command may be temporary. It adjusts the ships latitude upward by 45
        degrees.
    """

    key = "up"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):
        "Pitch ship up"
        self.obj.db.lat = (self.obj.db.lat + 45) % 360
        self.caller.msg("The ship is now oriented to {} latitude.".format(self.obj.db.lat))


class CmdSSCDown(Command):
    """
    Pitch the ship to down, 45 degrees

    Usage:
        down

    This command may be temporary. It adjusts the ships latitude downwards by 45
        degrees.
    """

    key = "down"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):
        "Pitch ship down"
        self.obj.db.lat = (self.obj.db.lat - 45 + 360) % 360
        self.caller.msg("The ship is now oriented to {} latitude.".format(self.obj.db.lat))
