########################################################################
# Copyright 2012 wst, wstcode@gmail.com
#
# This file is part of wstbot.
#
# wstbot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wstbot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with wstbot.  If not, see <http://www.gnu.org/licenses/>.
########################################################################

class Command:
    """Base class for commands"""

    def __init__(self, bot):
        """Initialize module"""
        if bot is None:
            self.enabled = False
            return
        self.enabled = True
        self.bot = bot
        self.msg_formats = self.bot.transport.msg_formats

    def do_cmd(self, argstr, nick):
        """
        Execute the command.

        Arguments:
        argstr -- argument string (for "!cmd a b c", argstr would be "a b c")
        nick -- nickname of the person who sent the command

        The return string will be sent to the active channel.
        """
        
        if self.enabled:
            return self.do(argstr, nick)
        
    def do(self, argstr, nick):
        """Do something."""
        return ""

    def get_cmd(self):
        """ Return the raw command """
        return ""

    def get_help(self):
        """ Return help for this specific command """
        return ""
