# world/

This folder is meant as a miscellanous folder for all that other stuff
related to the game. Code which are not commands or typeclasses go
here, like custom economy systems, combat code, batch-files etc.

You can restructure and even rename this folder as best fits your
sense of organisation. Just remember that if you add new sub
directories, you must add (optionally empty) `__init__.py` files in
them for Python to be able to find the modules within.

## Customizations

[space.py](space.py) - Expansion of wilderness contrib
 * Handles 3 dimensions
 * Removed the limitation of coordinates to positive numbers
 * Rooms now inherit from [typeclasses.object.Object](/typeclasses/objects.py)
   to provide exit sorting

[wilderness.py](wilderness.py) - Minor modification to the stock wilderness
contrib
 * Removed the limitation of coordinates to positive numbers
 * Rooms now inherit from [typeclasses.object.Object](/typeclasses/objects.py)
   to provide exit sorting
