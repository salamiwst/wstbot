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

class InformationSource:

    def __init__(self, bot):
        self.bot = bot
        self.msg_formats = self.bot.transport.msg_formats

    def find_info(self, url):
        """Retrieve a string of information that will be displayed by the bot
        after the link was posted.
        Returns a tuple (information message, raw title)"""
        return None

    def find_media_info(self, url):
        """Find out the type of the media item (the type determines how it is
        displayed on the web server media list.
        Returns a tuple (type, url)"""
        return None

