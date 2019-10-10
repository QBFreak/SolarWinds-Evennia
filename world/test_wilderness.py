from evennia import create_object
from evennia import DefaultCharacter
from evennia.utils.test_resources import EvenniaTest
from world import wilderness


class TestWilderness(EvenniaTest):

    def setUp(self):
        super(TestWilderness, self).setUp()
        self.char1 = create_object(DefaultCharacter, key="char1")
        self.char2 = create_object(DefaultCharacter, key="char2")

    def get_wilderness_script(self, name="default"):
        w = wilderness.WildernessScript.objects.get("default")
        return w

    def test_create_wilderness_default_name(self):
        wilderness.create_wilderness()
        w = self.get_wilderness_script()
        self.assertIsNotNone(w)

    def test_create_wilderness_custom_name(self):
        name = "customname"
        wilderness.create_wilderness(name)
        w = self.get_wilderness_script(name)
        self.assertIsNotNone(w)

    def test_enter_wilderness(self):
        wilderness.create_wilderness()
        wilderness.enter_wilderness(self.char1)
        self.assertIsInstance(self.char1.location, wilderness.WildernessRoom)
        w = self.get_wilderness_script()
        self.assertEqual(w.db.itemcoordinates[self.char1], (0, 0))

    def test_enter_wilderness_custom_coordinates(self):
        wilderness.create_wilderness()
        wilderness.enter_wilderness(self.char1, coordinates=(1, 2))
        self.assertIsInstance(self.char1.location, wilderness.WildernessRoom)
        w = self.get_wilderness_script()
        self.assertEqual(w.db.itemcoordinates[self.char1], (1, 2))

    def test_enter_wilderness_custom_name(self):
        name = "customnname"
        wilderness.create_wilderness(name)
        wilderness.enter_wilderness(self.char1, name=name)
        self.assertIsInstance(self.char1.location, wilderness.WildernessRoom)

    def test_wilderness_correct_exits(self):
        wilderness.create_wilderness()
        wilderness.enter_wilderness(self.char1)

        # By default we enter in the center (0, 0), all the exits should
        # be visible / traversable
        exits = [i for i in self.char1.location.contents
                 if i.destination and (
                     i.access(self.char1, "view") or
                     i.access(self.char1, "traverse"))]
        self.assertEqual(len(exits), 8)
        exitsok = ["north", "northeast", "east", "southeast", "south",
                   "southwest", "west", "northwest"]
        for each_exit in exitsok:
            self.assertTrue(any([e for e in exits if e.key == each_exit]))

    def test_room_creation(self):
        # Pretend that both char1 and char2 are connected...
        self.char1.sessions.add(1)
        self.char2.sessions.add(1)
        self.assertTrue(self.char1.has_account)
        self.assertTrue(self.char2.has_account)

        wilderness.create_wilderness()
        w = self.get_wilderness_script()

        # We should have no unused room after moving the first account in.
        self.assertEqual(len(w.db.unused_rooms), 0)
        w.move_obj(self.char1, (0, 0))
        self.assertEqual(len(w.db.unused_rooms), 0)

        # And also no unused room after moving the second one in.
        w.move_obj(self.char2, (1, 1))
        self.assertEqual(len(w.db.unused_rooms), 0)

        # But if char2 moves into char1's room, we should have one unused room
        # Which should be char2's old room that got created.
        w.move_obj(self.char2, (0, 0))
        self.assertEqual(len(w.db.unused_rooms), 1)
        self.assertEqual(self.char1.location, self.char2.location)

        # And if char2 moves back out, that unused room should be put back to
        # use again.
        w.move_obj(self.char2, (1, 1))
        self.assertNotEqual(self.char1.location, self.char2.location)
        self.assertEqual(len(w.db.unused_rooms), 0)

    def test_get_new_coordinates(self):
        loc = (1, 1)
        directions = {"north": (1, 2),
                      "northeast": (2, 2),
                      "east": (2, 1),
                      "southeast": (2, 0),
                      "south": (1, 0),
                      "southwest": (0, 0),
                      "west": (0, 1),
                      "northwest": (0, 2)}
        for direction, correct_loc in directions.items():  # Not compatible with Python 3
            new_loc = wilderness.get_new_coordinates(loc, direction)
            self.assertEqual(new_loc, correct_loc, direction)
