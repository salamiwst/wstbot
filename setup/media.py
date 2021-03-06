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

import sqlite3
import os

MEDIA_DB_PATH = os.path.join("data", "media.db")
MEDIA_TABLE = """create table media (
id integer primary key,
type text,
title text,
url text
);"""

class Media:

    def setup(self):
        self.setup_database()

    def setup_database(self):
        with sqlite3.connect(MEDIA_DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute(MEDIA_TABLE)
            conn.commit()

if __name__ == "__main__":
    Media().setup()

CLASS_ = Media
