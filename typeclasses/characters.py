"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
import random
from evennia import DefaultCharacter


class Character(DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """
    def at_object_creation(self):
        """
        Called only at initial creation. Give the user color and cname
        attributes. Color will set the line color in chat, and cname will set
        the color pattern of the name in chat. Eventually this will be extended
        to all of Evennia.
        """
        # TODO: Acquire colors the way @color does
        # (see evennia/commands/account.py CmdColorTest)
        colors = ['r', 'g', 'y', 'b', 'm', 'c', 'w']
        self.db.color = random.choice(colors)
        if random.choice([True, False]):
            self.db.color = self.db.color.upper()
        self.db.cname = None

    def get_color(self):
        """
        Simple access method to return color as a str
        """
        if self.db.color == None:
            return ""
        else:
            return str(self.db.color)

    def get_cname(self):
        """
        Simple access method to return cname as str
        Defaults to color if no cname is set
        """
        if self.db.cname == None or self.db.cname == "":
            return self.get_color()
        else:
            return str(self.db.cname)
