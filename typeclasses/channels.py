"""
Channel

The channel class represents the out-of-character chat-room usable by
Accounts in-game. It is mostly overloaded to change its appearance, but
channels can be used to implement many different forms of message
distribution systems.

Note that sending data to channels are handled via the CMD_CHANNEL
syscommand (see evennia.syscmds). The sending should normally not need
to be modified.

"""

import random
from evennia import DefaultChannel


class Channel(DefaultChannel):
    """
    Working methods:
        at_channel_creation() - called once, when the channel is created
        has_connection(account) - check if the given account listens to this channel
        connect(account) - connect account to this channel
        disconnect(account) - disconnect account from channel
        access(access_obj, access_type='listen', default=False) - check the
                    access on this channel (default access_type is listen)
        delete() - delete this channel
        message_transform(msg, emit=False, prefix=True,
                          sender_strings=None, external=False) - called by
                          the comm system and triggers the hooks below
        msg(msgobj, header=None, senders=None, sender_strings=None,
            persistent=None, online=False, emit=False, external=False) - main
                send method, builds and sends a new message to channel.
        tempmsg(msg, header=None, senders=None) - wrapper for sending non-persistent
                messages.
        distribute_message(msg, online=False) - send a message to all
                connected accounts on channel, optionally sending only
                to accounts that are currently online (optimized for very large sends)

    Useful hooks:
        channel_prefix(msg, emit=False) - how the channel should be
                  prefixed when returning to user. Returns a string
        format_senders(senders) - should return how to display multiple
                senders to a channel
        pose_transform(msg, sender_string) - should detect if the
                sender is posing, and if so, modify the string
        format_external(msg, senders, emit=False) - format messages sent
                from outside the game, like from IRC
        format_message(msg, emit=False) - format the message body before
                displaying it to the user. 'emit' generally means that the
                message should not be displayed with the sender's name.

        pre_join_channel(joiner) - if returning False, abort join
        post_join_channel(joiner) - called right after successful join
        pre_leave_channel(leaver) - if returning False, abort leave
        post_leave_channel(leaver) - called right after successful leave
        pre_send_message(msg) - runs just before a message is sent to channel
        post_send_message(msg) - called just after message was sent to channel

    """
    def channel_prefix(self, msg, emit=False):
        """
        Controls how the channel should be prefixed when returning to user.

        Args:
            msg (evennia.comms.models.TempMsg): Message object
            emit (bool, optional): Indicates the message is an emit

        Returns:
            display_channel (str): The formatted channel display name

        Notes:
            Colors the channel prefix based on the sender's `color` attribute
        """
        sender_color = ""
        if len(msg.senders) > 0:
            sender_color = msg.senders[0].get_color()
        if sender_color != "":
            sender_color = "|" + sender_color
        display_channel = "{0}[{1}] ".format(
            sender_color,
            " ".join(c.name for c in msg.channels)
        )
        return display_channel

    def format_message(self, msg, emit=False):
        """
        Format a message body before display it to the user

        Args:
            msg (evennia.comms.models.TempMsg): Message object
            emit (bool, optional): Indicates the message is an emit (supress
                 the player name)

         Returns:
            formatted_message (str): The formatted message text

        Notes:
            * Format the user name with color, per the user's `cname` attribute
            * Color the text with the user's `color` attribute
            * Handle pose, possessive pose, to, and thought bubbles

        Unimplemented:
            * Format the 'to' player's name with their `ctext`
        """
        formatted_message = ""
        if len(msg.senders) == 1:
            sender_color = msg.senders[0].get_color()
            sender_cname = msg.senders[0].get_cname()
            if sender_color == "":
                sender_color = "W"
            if sender_cname == "":
                sender_cname = "W"
            formatted_message = "{0}|{1}".format(
                self.format_ctext(msg.senders[0].name, sender_cname),
                sender_color
            )
        elif len(msg.senders) > 1:
            for sender in msg.senders:
                formatted_message = "{0}, {1}|{2}".format(
                    formatted_message,
                    self.format_ctext(sender.name, sender.get_cname()),
                    msg.senders[0].get_color()
                )
        if emit:
            formatted_message = "{1}".format(formatted_message, msg.message)
        else:
            if msg.message[0] == ":":
                formatted_message = "{0} {1}".format(
                    formatted_message,
                    msg.message[1:]
                )
            elif msg.message[0] == ";":
                formatted_message = "{0}'s {1}".format(
                    formatted_message,
                    msg.message[1:]
                )
            elif msg.message[0] == "'" and len(msg.message.split(' ')) > 1:
                words = msg.message.split(' ')
                user = words[0]
                del words[0]
                message_text = " ".join(words)
                formatted_message = "{0} [to: {2}]: {1}".format(
                    formatted_message,
                    message_text,
                    user[1:]
                )
            elif msg.message[0] == ".":
                bubble_color = random.choice(['w', 'c', 'y'])
                formatted_message = "{0} |x. |Co |cO |w( |{2}{1} |w)".format(
                    formatted_message,
                    msg.message[1:],
                    bubble_color
                )
            else:
                formatted_message = "{0}: {1}".format(
                    formatted_message,
                    msg.message
                )
        return formatted_message

    def format_ctext(self, text, cformat):
        """
        Format a string of text with colors based on `ctext` style formatting

        Args:
            text (str): The text to format
            cformat (str): The ctext formatting

        Returns:
            formatted_text (str): A string of text formatted with Evennia style
                color formatting

        Example:
            format_ctext("Hello!", "r,g")
        """
        if len(cformat) < 1:
            return text
        if len(cformat.split(',')) == 1:
            return "|{0}{1}".format(cformat, text)
        colors = cformat.split(',')
        color_ptr = 0
        formatted_text = ""
        text_ptr = 0
        skip = 1
        while text_ptr < len(text):
            if len(colors[color_ptr].split(':')) == 2:
                color = colors[color_ptr].split(':')[0]
                skip = int(colors[color_ptr].split(':')[1])
            else:
                color = colors[color_ptr]
                skip = 1
            if skip == 1:
                formatted_text = formatted_text + "|{0}{1}".format(color, text[text_ptr])
                text_ptr += 1
            else:
                formatted_text = formatted_text + "|{0}".format(color)
                for i in range(
                            text_ptr,
                            self.clip(text_ptr + skip, text_ptr, len(text))
                        ):
                    formatted_text = formatted_text + text[i]
                text_ptr += skip
            color_ptr += 1
            if color_ptr >= len(colors):
                color_ptr = 0
        return formatted_text

    def clip(self, a, a_min, a_max):
        """
        Limit a value or list to a specific set of bounds

        Args:
            a (list): The list of values to limit
            a_min (int): The minimum value that may be present in the list
            a_max (int): The maximum value that may be present in the list

        Returns:
            a (array): The array of values, none lesser than a_min and none
                greater than a_max

        Example:
            clip(value, 0, 10)
            clip(values, 0, 10)
        """
        if a_min >= a_max:
            raise ValueError("clip: a_min must be less than a_max.")
        if isinstance(a, list):
            for i in range(len(a)):
                if a[i] < a_min:
                    a[i] = a_min
                if a[i] > a_max:
                    a[i] = a_max
        else:
            if a < a_min:
                a = a_min
            if a > a_max:
                a = a_max
        return a
