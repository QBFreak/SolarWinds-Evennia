"""
SpaceShipConsole Commands

These are the commands and command set for the SpaceShipConsole
"""

from evennia import CmdSet
from evennia import Command


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
            if not self.obj.db.lat:
                self.obj.db.lat = 0
            caller.msg("The current longitude is {}".format(self.obj.db.lat))
        else:
            if int(self.target) % 45 != 0:
                caller.msg("Longitude must be entered in increments of 45 degrees")
            else:
                self.obj.db.lat = int(self.target)
                caller.msg("The current longitude has been set to {}".format(self.obj.db.lat))
