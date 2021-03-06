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

# -*- coding: utf-8 -*-

import socket
import re
import logging
from wstbot_locals import STREAM_LOG_FORMAT, FILE_LOG_FORMAT

ENCODING = "utf-8"
FILE_LOG = "wirc.log"

logger = logging.getLogger(__name__)

class wIRC:
    """IRC client with minimal features"""

    def __init__(self, server, nick, port=6667, ident='wIRC', realname='wIRC bot', debug=False):
        self.server = server
        self.nick = nick
        self.port = port
        self.ident = ident
        self.realname = realname
        
        self.connected = False

        # initialize logger
        self.debug = debug # sets self._debug
        # stream handler
        stream_handler = logging.StreamHandler()
        stream_formatter = logging.Formatter(STREAM_LOG_FORMAT)
        stream_handler.setFormatter(stream_formatter)
        # file handler
        file_handler = logging.FileHandler(FILE_LOG)
        file_formatter = logging.Formatter(FILE_LOG_FORMAT)
        file_handler.setFormatter(file_formatter)
        # add handlers
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        self._debug = value
        if self._debug:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
        
    def connect(self):
        """Connect to server"""
        
        if self.connected:
            return
            
        self.connected = False
        try:
            self.sock = socket.socket()
            self.sock.connect((self.server, self.port))
            logger.info("Connected to {}:{}!".format(self.server, self.port))
        except:
            logger.error("Could not connect to {}!".format(self.server))
            return
            
        self.connected = True
        self.send_nick()
        self.send_user()
        
        self.on_connected()
            
    def run(self):
        """This has to be called after connecting"""
        while True:
            self.doirc()
            
    def doirc(self):
        rdata = self.sock.recv(1024)
        strdata = self.chain_decode(rdata)
        if strdata is None:
            return
        lines = strdata.split("\n")

        for line in lines:
            line=line.rstrip()
            if line == "":
                continue
            logger.debug("<- {0}".format(line))
            self.on_receive(line)

            words=line.split(" ")
            
            if words[0] == "PING":
                self.send("PONG {0}\n".format(words[1]))
            elif len(words) > 1 and words[1] == "JOIN":
                nick, ident, server, channel = re.match(":(.*)!(.*)@(.*) JOIN (.*)", line).groups()
                if nick == self.nick:
                    self.on_me_join(channel)
                else:
                    self.on_join(nick, ident, server)
            elif len(words) > 1 and words[1] == "PRIVMSG":
                match = re.match(":(.*)!(.*)@(.*) PRIVMSG (.*) :(.*)", line)
                if match is None:
                    logger.warning("privmsg match was None!")
                privmsgdata = match.groups()
                nick = privmsgdata[0]
                ident = privmsgdata[1]
                server = privmsgdata[2]
                target = privmsgdata[3]
                msg = privmsgdata[4]
                
                self.on_privmsg(nick, ident, server, target, msg)

    def chain_decode(self, data):
        # try default encoding
        try:
            strdata = data.decode(ENCODING)
            return strdata
        except UnicodeDecodeError:
            logger.exception("decoding with default encoding failed")

        # try latin
        try:
            strdata = data.decode("latin_1")
            return strdata
        except UnicodeDecodeError:
            logger.exception("decoding with latin encoding failed")

        # do unicode with replacement
        try:
            strdata = data.decode("utf-8", "replace")
            return strdata
        except:
            logger.error("utf-8 decoding with replacement failed!")
                    
    def disconnect(self):
        self.sock.disconnect()
        
    def quit(self):
        self.disconnect()

    def on_join(self, nick, ident, server):
        pass

    def on_receive(self, line):
        pass

    def on_connected(self):
        pass
        
    def on_privmsg(self, nick, ident, server, target, msg):
        pass
        
    def join(self, chan):
        self.send("JOIN {}\n".format(chan))
        #self.on_me_join(chan)

    def part(self, chan):
        self.send("PART {}\n".format(chan))
        
    def on_me_join(self, channel):
        pass
        
    def disconnect(self):
        if self.connected:
            self.sock.close()
            
    def send(self, message):
        self.sock.send(message.encode(ENCODING))
        logger.debug("-> {0}".format(message))
        
    def msg(self, target, message):
        self.send("PRIVMSG {0} :{1}\n".format(target, message))
        logger.debug("Msg: ({0}) {1}".format(target, message))
            
    def send_nick(self):
        self.send("NICK " + self.nick + "\n")
        
    def send_user(self):
        self.send("USER {0} {1} awsm :{2}\n".format(self.ident, self.server, self.realname))
