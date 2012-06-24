#!/usr/bin/python 
#**************************************************************************************
# VashyTheNexian
# Project start date - 06/22/2012
# 
#
#**************************************************************************************
import sys
import signal # For Ctrl + C signal handler
import socket
import string
import re
import ConfigParser


#**************************************************************************************
# This function handles the closing of the bot from the CLI using Ctrl+C
# It makes sure the socket gets closed
#**************************************************************************************
def signal_handler(signal, frame):
	print 'Now exiting because of Ctrl + C'
	s.close()
	sys.exit(0)	

signal.signal(signal.SIGINT, signal_handler)

#**************************************************************************************
# After NICK, the server sends PING :<random number> to you, which has to be replied with 
# PONG :<same number>. Then you may send USER, the registration process is done 
# and raw 001 or an ERROR (klined, server full, etc.) is sent to you. The server also sends 
#PINGs in the same way with a certain interval, which have to be replied in the same way.
#**************************************************************************************
def sUSERNICK(s, NICK):
	s.send('NICK '+NICK + "\r\n")
	
	
#**************************************************************************************
# This function returns the desired value from the config file
#**************************************************************************************
def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1
	
#**************************************************************************************
# Setup ConfigParser object
#**************************************************************************************
configFilename = 'settings.config'
Config = ConfigParser.SafeConfigParser()
Config.read(configFilename)

#**************************************************************************************
# Pull data from config file
#**************************************************************************************
HOST = ConfigSectionMap('irc')['host']
NICK = ConfigSectionMap('irc')['nick']
PORT = int(ConfigSectionMap('irc')['port'])
CHANNELINIT = ConfigSectionMap('irc')['channelinit']
REALNAME = ConfigSectionMap('irc')['realname']
PASS = ConfigSectionMap('irc')['pass']

#**************************************************************************************
# Create socket and connect to server
#**************************************************************************************
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((HOST, PORT))

#**************************************************************************************
# If socket is null, exit
#**************************************************************************************
if s is None:
	print "Socket error while connecting"
	exit()
	
try :
	line = s.recv(512) #s.recv() will never return None
	while (line != ""):
		print line #server message is output to screen
		if line.find("No ident response") != -1:
			sUSERNICK(s, NICK)
			
		if line.find("PING :") != -1:
			pingrequest = re.search("PING :(.+)", line)
			s.send("PONG :" + pingrequest.group(1))
			s.send('USER ' +NICK + ' ' + NICK + ' ' + NICK + ' : ' + REALNAME + '\r\n')
			s.send('AUTH ' + NICK + ' ' + PASS + '\r\n')
			s.send('JOIN #'+CHANNELINIT + "\r\n") #Joins default channel
			
		if line.find("001") != -1:
			print "Successfully connected!"
			
		if line.find("Hello " + NICK) != -1:
			s.send("Hello! :) I am nex-bot <3")
		line = s.recv(512)		
	s.close()
	print "Exiting now"
	exit()
except Exception, err:
	print "MY ERROR: " + str(err)
	s.close()
	exit()
