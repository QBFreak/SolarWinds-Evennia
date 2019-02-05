# typeclasses/

This directory holds the modules for overloading all the typeclasses
representing the game entities and many systems of the game. Other
server functionality not covered here is usually modified by the
modules in `server/conf/`.

Each module holds empty classes that just imports Evennia's defaults.
Any modifications done to these classes will overload the defaults.

You can change the structure of this directory (even rename the
directory itself) as you please, but if you do you must add the
appropriate new paths to your settings.py file so Evennia knows where
to look. Also remember that for Python to find your modules, it
requires you to add an empty `__init__.py` file in any new sub
directories you create.

## Customizations

[channelcommands.py](channelcommands.py) - Allow channel commands and aliases
to work without any whitespace between them and the message to the channel.
For instance:

```
=This is my message
[Public] root: This is my message
```

Where the default behavior required the command to be `= This is my message.`

[channels.py](channels.py) - Color formatting for channel text based on a
user's `@color` and `@ctext` attributes. Ripped off straight from TinyMARE :)

[characters.py](characters.py)
 * The `@color` attribute defaults to a random color on character creation
 * player objects inherit from [objects.py](objects.py).Object to provide
   colored object names when using `look` command (`return_appearance()`)

[exits.py](exits.py) - exit objects inherit from
[objects.py](objects.py).Object to provide colored object names when using
`look` command (`return_appearance()`)

[rooms.py](rooms.py) - room objects inherit from
[objects.py](objects.py).Object to provide colored object names when using
`look` command (`return_appearance()`)

[objects.py](objects.py) - default object provides `return_appearance()` hook
to format object names with colors based on `@color` attribute when a player
`look`s

[spaceship.py](spaceship.py) - Typeclasses for ships that travel through Space.

[test_characters.py](test_characters.py) - Unit tests for
[characters.py](characters.py). Ensures default values for new characters are
set properly.

[test_objects.py](test_objects.py) - Unit tests for [objects.py](objects.py).
 * Ensures that `Characters`, `Exits` and `Rooms` all inherit from
  `typeclasses.objects.Object`
 * Ensures proper handling of color formatting of objects when
   `Object.return_appearance()` is called.
 * Ensures exits are ordered properly when `Object.return_appearance()` is
   called.
