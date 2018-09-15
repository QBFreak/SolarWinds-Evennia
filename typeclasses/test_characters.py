from evennia import create_object
from evennia.utils.test_resources import EvenniaTest
from typeclasses.rooms import Room
from typeclasses.characters import Character


class TestCharacterAtColor(EvenniaTest):

    """Unittest for character's `color` attribute"""

    def setUp(self):
        super(TestCharacterAtColor, self).setUp()
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
