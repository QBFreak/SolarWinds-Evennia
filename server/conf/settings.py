"""
Evennia settings file.

The available options are found in the default settings file found
here:

/data/chiana/Projects/evennia/evennia/settings_default.py

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "solarwinds"

# A list of ports the Evennia telnet server listens on Can be one or many.
TELNET_PORTS = [4400]

######################################################################
# In-game Channels created from server start
######################################################################

# This is a list of global channels created by the
# initialization script the first time Evennia starts.
# The superuser (user #1) will be automatically subscribed
# to all channels in this list. Each channel is described by
# a dictionary keyed with the same keys valid as arguments
# to the evennia.create.create_channel() function.
# Note: Evennia will treat the first channel in this list as
# the general "public" channel and the second as the
# general "mud info" channel. Other channels beyond that
# are up to the admin to design and call appropriately.
DEFAULT_CHANNELS = [
    # public channel
    {"key": "Public",
     "aliases": ('ooc', 'pub', '='),
     "desc": "Public discussion",
     "locks": "control:perm(Admin);listen:all();send:all()"},
    # connection/mud info
    {"key": "MudInfo",
     "aliases": "",
     "desc": "Connection log",
     "locks": "control:perm(Developer);listen:perm(Admin);send:false()"}
]

######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
