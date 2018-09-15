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
    """

    object_typeclass = Object
    character_typeclass = Character
    exit_typeclass = Exit
    room_typeclass = Room

    def setUp(self):
        super(TestObject, self).setUp()
        self.room = create_object(Room, key="Location")
        self.exit1 = create_object(
            Exit,
            key="Exit",
            location=self.room,
            destination=self.room
        )
        self.character = create_object(
            Character,
            key="Character",
            location=self.room
        )
        self.object2 = create_object(
            Object,
            key="Object2",
            location=self.room
        )

    def test_inheritance_character(self):
        """Test the inheritance of the Character object"""
        assert isinstance(self.character, Object)

    def test_inheritance_exit(self):
        """Test the inheritance of the Exit object"""
        assert isinstance(self.exit, Object)

    def test_inheritance_room(self):
        """Test the inheritance of the Room object"""
        assert isinstance(self.room, Object)


class TestObjectAppearance(EvenniaTest):
    """
    Unittest for default object appearance

    Tests the color formatting returned by Object.return_appearance()

     * The room is `r`
     * Exit 1 is the same color as the room
     * Exit 2 is `g`
     * Object is `c`
     * Commas between exits, objects should be `n`
     * We should end with `n` to be polite to whomever comes next
    """

    object_typeclass = Object
    character_typeclass = Character
    exit_typeclass = Exit
    room_typeclass = Room

    def setUp(self):
        super(TestObjectAppearance, self).setUp()
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

    def test_room_appearance(self):
        """Test the appearance of a room"""
        # print(self.room.return_appearance(self.character))
        assert self.room.return_appearance(self.character) == (
            "|rLocation|n\n"
            "\n"
            "|wExits:|n |rExit1|n, |gExit2|n\n"
            "|wYou see:|n |cObject1|n, |yObject2|n"
        )


class TestObjectExitOrder(EvenniaTest):
    """
    Unittest for default object exit ordering

    Tests the exit ordering returned by Object.return_appearance()

     * Exits should be arranged according to the following list
     * Exits not on the list should be left unordered at the end of the list
     * Case should be irrelevant

    *  west
    *  northwest
    *  southwest
    *  north
    *  up
    *  down
    *  south
    *  northeast
    *  southeast
    *  east
    """

    character_typeclass = Character
    exit_typeclass = Exit
    room_typeclass = Room

    def setUp(self):
        super(TestObjectExitOrder, self).setUp()
        self.room = create_object(Room, key="Location")

        # We should probably automate and randomize this...
        self.southeast = create_object(
            Exit,
            key="Southeast",
            location=self.room,
            destination=self.room
        )

        self.northwest = create_object(
            Exit,
            key="Northwest",
            location=self.room,
            destination=self.room
        )

        self.west = create_object(
            Exit,
            key="west",
            location=self.room,
            destination=self.room
        )

        self.south = create_object(
            Exit,
            key="south",
            location=self.room,
            destination=self.room
        )

        self.down = create_object(
            Exit,
            key="down",
            location=self.room,
            destination=self.room
        )

        self.northeast = create_object(
            Exit,
            key="northeast",
            location=self.room,
            destination=self.room
        )

        self.north = create_object(
            Exit,
            key="north",
            location=self.room,
            destination=self.room
        )

        self.somewhere = create_object(
            Exit,
            key="Somewhere",
            location=self.room,
            destination=self.room
        )

        self.southwest = create_object(
            Exit,
            key="southwest",
            location=self.room,
            destination=self.room
        )

        self.east = create_object(
            Exit,
            key="EAST",
            location=self.room,
            destination=self.room
        )

        self.up = create_object(
            Exit,
            key="uP",
            location=self.room,
            destination=self.room
        )

        self.character = create_object(
            Character,
            key="Character",
            location=self.room
        )

    def test_exit_order(self):
        """Test the ordering of exits"""
        # print(self.room.return_appearance(self.character))
        assert self.room.return_appearance(self.character) == (
            "|nLocation|n\n"
            "\n"
            "|wExits:|n |nwest|n, |nNorthwest|n, |nsouthwest|n, |nnorth|n, "
            "|nuP|n, |ndown|n, |nsouth|n, |nnortheast|n, |nSoutheast|n, "
            "|nEAST|n, |nSomewhere|n"
        )
