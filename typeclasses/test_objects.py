from evennia import create_object
from evennia.commands.default.tests import CommandTest
from evennia.utils.test_resources import EvenniaTest
from typeclasses.characters import Character
from typeclasses.exits import Exit
from typeclasses.objects import Object
from typeclasses.rooms import Room


class TestObject(EvenniaTest):
    """
    Unittest for default object

    Characters, Exits and Rooms should all inherit from
    typeclasses.objects.Object

    Tests the color formatting returned by Object.return_appearance() as
    specified in detail in test_room_appearance() below
    """

    object_typeclass = Object
    character_typeclass = Character
    exit_typeclass = Exit
    room_typeclass = Room

    def setUp(self):
        super(TestObject, self).setUp()
        self.room = create_object(Room, key="Location")
        self.room.db.color = 'r'
        self.exit1 = create_object(
            Exit,
            key="Exit1",
            location=self.room,
            destination=self.room
        )
        self.exit2 = create_object(
            Exit,
            key="Exit2",
            location=self.room,
            destination=self.room
        )
        self.exit2.db.color = 'g'
        self.character = create_object(
            Character,
            key="Character",
            location=self.room
        )
        self.object1 = create_object(
            Object,
            key="Object1",
            location=self.room
        )
        self.object1.db.color = 'c'
        self.object2 = create_object(
            Object,
            key="Object2",
            location=self.room
        )
        self.object2.db.color = 'y'

    def test_inheritance_character(self):
        """Test the inheritance of the Character object"""
        assert isinstance(self.character, Object)

    def test_inheritance_exit(self):
        """Test the inheritance of the Exit object"""
        assert isinstance(self.exit1, Object)

    def test_inheritance_room(self):
        """Test the inheritance of the Room object"""
        assert isinstance(self.room, Object)

    def test_room_appearance(self):
        """
        Test the appearance of a room

        As set above in setUp:
         * The room name is `r`
         * Exit 1 is the same color as the room
         * Exit 2 is `g`
         * Object is `c`
         * Commas between exits, objects should be `n`
         * We should end with `n` to be polite to whomever comes next
        """
        # print(self.room.return_appearance(self.character))
        assert self.room.return_appearance(self.character) == \
            "|rLocation|n\n\n|wExits:|n |rExit1|n, |gExit2|n\n|wYou see:|n |cObject1|n, |yObject2|n"
