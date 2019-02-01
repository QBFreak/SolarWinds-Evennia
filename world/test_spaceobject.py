from evennia import create_object
from evennia import DefaultCharacter
from evennia.utils.test_resources import EvenniaTest
from world import space
from world import spaceobject


class TestSpaceObject(EvenniaTest):
    """
    Unit tests for SpaceObject.

    Tests:
     -
    """
    def setUp(self):
        super(TestSpaceObject, self).setUp()
        self.char1 = create_object(DefaultCharacter, key="char1")
        self.char2 = create_object(DefaultCharacter, key="char2")
        space.create_space()
        space.enter_space(self.char1, coordinates=(1, 2, 3))
        # self.assertIsInstance(self.char1.location, space.SpaceRoom)
        # s = self.get_space_script()
        # self.assertEquals(s.db.itemcoordinates[self.char1], (0, 0, 0))

    def get_space_script(self, name="default"):
        s = space.SpaceScript.objects.get("default")
        return s

    def space_object_repeatability_test(self, space_object):
        objs = []
        # Check for repeatability of results, regardless of creation order
        for i in range(-10, 11):
            for j in range(-10, 11):
                for k in range(-10, 11):
                    if space_object.object_at_coordinates((i, j, k)):
                        objs.append((i, j, k))
        for i in range(10, -11, -1):
            for j in range(10, -11, -1):
                for k in range(10, -11, -1):
                    if space_object.object_at_coordinates((i, j, k)):
                        if (i, j, k) in objs:
                            pass
                        else:
                            raise Exception("Object found at coordinates that should be empty!")
                    else:
                        if (i, j, k) in objs:
                            raise Exception(
                                "No object found at coordinates that should not be empty!"
                            )

    def test_space_object(self):
        self.space_object_repeatability_test(spaceobject.Star())
        self.space_object_repeatability_test(spaceobject.Planet())
        self.space_object_repeatability_test(spaceobject.Moon())
