from evennia import create_object
from evennia.utils.test_resources import EvenniaTest
from typeclasses.rooms import Room
from typeclasses.characters import Character


class TestCharacterDefaultAttributes(EvenniaTest):
    """
    Unittest for character default attributes

    Newly created characters are assigned a value to their `color` attribute,
    chosen at random from a list of valid colors. In addition this color could
    be bold (lowercase) or regular (uppercase). We check to make sure that the
    color in the `color` attribute is on the list, regardless of it's case.

    Newly created characters are assigned a value of `None` to their `cname`
    attribute. We check to ensure this is the case.

    get_color() should return the `color` attribute

    get_cname() should return the `cname` attribute
    """

    def setUp(self):
        super(TestCharacterDefaultAttributes, self).setUp()
        self.room = create_object(Room, key="Location")
        self.character = create_object(
            Character,
            key="Character",
            location=self.room
        )

    def test_at_color(self):
        """Test the `color` attribute"""
        colors = ['r', 'g', 'y', 'b', 'm', 'c', 'w']
        assert self.character.db.color.lower() in colors

    def test_at_cname(self):
        """Test the `cname` attribute"""
        assert self.character.db.cname is None

    def test_get_color(self):
        """Test the get_color() method"""
        assert self.character.db.color == self.character.get_color()

    def test_get_cname(self):
        """Test the get_cname() method"""
        # We assign a value to `cname` first, since the default is `None`
        self.character.db.cname = "r,g"
        assert self.character.db.cname == self.character.get_cname()
