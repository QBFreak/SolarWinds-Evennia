from evennia import create_object
from evennia import DefaultCharacter
from evennia.utils.test_resources import EvenniaTest
from world import space


class TestSpace(EvenniaTest):
    """
    Unit tests for Space. A modification of unit tests for Wilderness Contrib
        Only minor changes were required to make this work for Space, mostly
        new names and additional exits.

    Tests:
     - Creation of Space with default name
     - Creation of Space with custom name
     - A PC entering space at the default coordinates
     - A PC entering space at specific coodinates
     - A PC entering space where space has a custom name
     - Space has the correct exits
     - Room creation, including splitting and combining rooms as PCs move
     - Verifying new coordinates are correct as a PC uses each exit
    """
    def setUp(self):
        super(TestSpace, self).setUp()
        self.char1 = create_object(DefaultCharacter, key="char1")
        self.char2 = create_object(DefaultCharacter, key="char2")

    def get_space_script(self, name="default"):
        s = space.SpaceScript.objects.get("default")
        return s

    def test_create_space_default_name(self):
        space.create_space()
        s = self.get_space_script()
        self.assertIsNotNone(s)

    def test_create_space_custom_name(self):
        name = "customname"
        space.create_space(name)
        s = self.get_space_script(name)
        self.assertIsNotNone(s)

    def test_enter_space(self):
        space.create_space()
        space.enter_space(self.char1)
        self.assertIsInstance(self.char1.location, space.SpaceRoom)
        s = self.get_space_script()
        self.assertEqual(s.db.itemcoordinates[self.char1], (0, 0, 0))

    def test_enter_space_custom_coordinates(self):
        space.create_space()
        space.enter_space(self.char1, coordinates=(1, 2, 3))
        self.assertIsInstance(self.char1.location, space.SpaceRoom)
        s = self.get_space_script()
        self.assertEqual(s.db.itemcoordinates[self.char1], (1, 2, 3))

    def test_enter_space_custom_name(self):
        name = "customnname"
        space.create_space(name)
        space.enter_space(self.char1, name=name)
        self.assertIsInstance(self.char1.location, space.SpaceRoom)

    def test_space_correct_exits(self):
        space.create_space()
        space.enter_space(self.char1)

        # By default we enter in the center (0, 0, 0), so all exits should
        # be visible / traversable
        # TODO: Double check that there's no case of fewer exits (IE corners)
        space.enter_space(self.char1, coordinates=(0, 0, 0))
        exits = [i for i in self.char1.location.contents
                 if i.destination and (
                     i.access(self.char1, "view") or
                     i.access(self.char1, "traverse"))]
        self.assertEqual(len(exits), 10)
        exitsok = ["north", "northeast", "east", "southeast", "south",
                   "southwest", "west", "northwest", "up", "down"]
        for each_exit in exitsok:
            self.assertTrue(any([e for e in exits if e.key == each_exit]))

    def test_room_creation(self):
        # Pretend that both char1 and char2 are connected...
        self.char1.sessions.add(1)
        self.char2.sessions.add(1)
        self.assertTrue(self.char1.has_account)
        self.assertTrue(self.char2.has_account)

        space.create_space()
        s = self.get_space_script()

        # We should have no unused room after moving the first account in.
        self.assertEqual(len(s.db.unused_rooms), 0)
        s.move_obj(self.char1, (0, 0, 0))
        self.assertEqual(len(s.db.unused_rooms), 0)

        # And also no unused room after moving the second one in.
        s.move_obj(self.char2, (1, 1, 1))
        self.assertEqual(len(s.db.unused_rooms), 0)

        # But if char2 moves into char1's room, we should have one unused room
        # Which should be char2's old room that got created.
        s.move_obj(self.char2, (0, 0, 0))
        self.assertEqual(len(s.db.unused_rooms), 1)
        self.assertEqual(self.char1.location, self.char2.location)

        # And if char2 moves back out, that unused room should be put back to
        # use again.
        s.move_obj(self.char2, (1, 1, 1))
        self.assertNotEqual(self.char1.location, self.char2.location)
        self.assertEqual(len(s.db.unused_rooms), 0)

    def test_get_new_coordinates(self):
        loc = (1, 1, 1)
        directions = {"north": (1, 2, 1),
                      "northeast": (2, 2, 1),
                      "east": (2, 1, 1),
                      "southeast": (2, 0, 1),
                      "south": (1, 0, 1),
                      "southwest": (0, 0, 1),
                      "west": (0, 1, 1),
                      "northwest": (0, 2, 1),
                      "up": (1, 1, 2),
                      "down": (1, 1, 0)}
        for direction, correct_loc in directions.items():  # Not compatible with Python 3
            new_loc = space.get_new_coordinates(loc, direction)
            self.assertEqual(new_loc, correct_loc, direction)
