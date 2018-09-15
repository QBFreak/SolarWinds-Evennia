from evennia import create_channel
from evennia import create_object
from evennia.comms.models import TempMsg
from evennia.utils.test_resources import EvenniaTest
from typeclasses.channels import Channel
from typeclasses.characters import Character
from typeclasses.rooms import Room


class TestChannel(EvenniaTest):
    """
    Unittest for Channel object

    Channel.channel_prefix() should format channel name with `color` attribute
    of first sender

    Channel.format_message() performs multiple formatting options depending
    on the message provided
    * Always format the message text with the `color` attribute  of the first
      sender
    * Format the sender names according to their `ctext` attributes
    * Format the beginning of the message based on:
       * Emotes
       * Possessive Emotes
       * To:
       * Thought Bubbles
    """

    character_typeclass = Character
    room_typeclass = Room

    def setUp(self):
        super(TestChannel, self).setUp()
        self.room = create_object(Room, key="Location")
        self.character = create_object(
            Character,
            key="TEST",
            location=self.room
        )
        self.character.db.color = 'c'
        self.character.db.cname = 'r,g'
        self.channel = create_channel(key="Foo", typeclass=Channel)
        self.tempmsg = TempMsg(
            senders=self.character,
            channels=self.channel,
            message="This is a test."
        )

    def test_channel_prefix(self):
        """Test the channel prefix formatting"""
        assert self.channel.channel_prefix(self.tempmsg) == \
            "|{1}[{0}] ".format(self.tempmsg.channels[0].name, self.character.db.color)

    def test_format_message(self):
        """Test the channel message formatting"""
        assert self.channel.format_message(self.tempmsg) == \
            "|rT|gE|rS|gT|{1}: {0}".format(
                self.tempmsg.message,
                self.character.db.color
            )
