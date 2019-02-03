from builtins import object

from evennia.commands import command
from evennia.utils.logger import tail_log_file
from django.utils.translation import ugettext as _

_CHANNELDB = None


class ChannelCommand(command.Command):
    """
    {channelkey} channel

    {channeldesc}

    Usage:
       {lower_channelkey}  <message>
       {lower_channelkey}<message>
       {lower_channelkey}/history [start]
       {lower_channelkey} off - mutes the channel
       {lower_channelkey} on  - unmutes the channel

    Switch:
        history: View 20 previous messages, either from the end or
            from <start> number of messages from the end.

    Example:
        {lower_channelkey} Hello World!
        {lower_channelkey}:waves
        {lower_channelkey}/history
        {lower_channelkey}/history 30

    """
    # ^note that channeldesc and lower_channelkey will be filled
    # automatically by ChannelHandler

    # this flag is what identifies this cmd as a channel cmd
    # and branches off to the system send-to-channel command
    # (which is customizable by admin)
    is_channel = True
    key = "general"
    help_category = "Channel Names"
    obj = None
    # Changed arg_regex to make whitespace between channel command/alias and
    # message/subcommand optional
    arg_regex = r"\s?.*?|/history.*?"

    def parse(self):
        """
        Simple parser
        """
        # cmdhandler sends channame:msg here.
        channelname, msg = self.args.split(":", 1)
        self.history_start = None
        if msg.startswith("/history"):
            arg = msg[8:]
            try:
                self.history_start = int(arg) if arg else 0
            except ValueError:
                # if no valid number was given, ignore it
                pass
        self.args = (channelname.strip(), msg.strip())

    def func(self):
        """
        Create a new message and send it to channel, using
        the already formatted input.
        """
        global _CHANNELDB
        if not _CHANNELDB:
            from evennia.comms.models import ChannelDB as _CHANNELDB

        channelkey, msg = self.args
        caller = self.caller
        if not msg:
            self.msg(_("Say what?"))
            return
        channel = _CHANNELDB.objects.get_channel(channelkey)

        if not channel:
            self.msg(_("Channel '%s' not found.") % channelkey)
            return
        if not channel.has_connection(caller):
            string = _("You are not connected to channel '%s'.")
            self.msg(string % channelkey)
            return
        if not channel.access(caller, 'send'):
            string = _("You are not permitted to send to channel '%s'.")
            self.msg(string % channelkey)
            return
        if msg == "on":
            caller = caller if not hasattr(caller, 'account') else caller.account
            unmuted = channel.unmute(caller)
            if unmuted:
                self.msg("You start listening to %s." % channel)
                return
            self.msg("You were already listening to %s." % channel)
            return
        if msg == "off":
            caller = caller if not hasattr(caller, 'account') else caller.account
            muted = channel.mute(caller)
            if muted:
                self.msg("You stop listening to %s." % channel)
                return
            self.msg("You were already not listening to %s." % channel)
            return
        if self.history_start is not None:
            # Try to view history
            log_file = channel.attributes.get("log_file", default="channel_%s.log" % channel.key)

            def send_msg(lines): return self.msg("".join(line.split("[-]", 1)[1]
                                                         if "[-]" in line else line for line in lines))
            tail_log_file(log_file, self.history_start, 20, callback=send_msg)
        else:
            caller = caller if not hasattr(caller, 'account') else caller.account
            if caller in channel.mutelist:
                self.msg("You currently have %s muted." % channel)
                return
            channel.msg(msg, senders=self.caller, online=True)

    def get_extra_info(self, caller, **kwargs):
        """
        Let users know that this command is for communicating on a channel.

        Args:
            caller (TypedObject): A Character or Account who has entered an ambiguous command.

        Returns:
            A string with identifying information to disambiguate the object, conventionally with a preceding space.
        """
        return _(" (channel)")
