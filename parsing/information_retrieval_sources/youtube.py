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

import logging
import re
from wstbot_locals import URL_REGEX_PREFIX
from util import download_page_decoded
from parsing.information_retrieval_sources.information_source import InformationSource

logger = logging.getLogger("wstbot")

class Youtube(InformationSource):

    def __init__(self, *args):
        super().__init__(*args)
        self.video_id = None

    def find_info(self, url):
        # valid youtube url?
        match_normal = re.match(URL_REGEX_PREFIX + "youtube\.com/watch.*v=(\S{11})", url)
        match_short = re.search(URL_REGEX_PREFIX + "youtu\.be/(\S+)", url)
        match = match_normal or match_short
        if match is None:
            return

        logger.info("Found youtube video: " + self.video_id)
        self.video_id = match.group(1)

        # find info
        content = download_page_decoded(url)
        if content is None:
            return

        match_title = re.search('<meta property="og:title" content="(.+)"\s*>', content)
        match_duration = re.search('<meta itemprop="duration" content="PT(.+)"\s*>', content)
        if (match_title and match_duration) is None:
            return

        raw_title = match_title.group(1)
        title = self.msg_formats.bold(self.msg_formats.red(raw_title))
        duration = match_duration.group(1)
        duration = duration.replace("M", "m ")
        duration = duration.replace("S", "s ")
        duration = duration.replace("H", "h ")
        duration = self.msg_formats.green(duration)

        message = "{0} :: {1}".format(title, duration)

        return (message, raw_title)

    def find_media_info(self, url):
        if self.video_id is not None:
            return ("youtube", self.video_id)
        else:
            return None

CLASS_ = Youtube