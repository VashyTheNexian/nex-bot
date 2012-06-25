#!/usr/bin/python 
#**************************************************************************************
# VashyTheNexian
# Project start date - 06/22/2012
# 
#
#**************************************************************************************
import sys
import socket
import string
import re
import ConfigParser

#**************************************************************************************
# After NICK, the server sends PING :<random number> to you, which has to be replied with 
# PONG :<same number>. Then you may send USER, the registration process is done 
# and raw 001 or an ERROR (klined, server full, etc.) is sent to you. The server also sends 
#PINGs in the same way with a certain interval, which have to be replied in the same way.
#**************************************************************************************
def sUSERNICK(s, NICK):
	s.sendall('NICK '+NICK + "\r\n")
	
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
# Example can be found here: http://wiki.python.org/moin/ConfigParserExamples
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
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	s.connect((HOST, PORT))
except Exception, err:
	print "Error connecting to " + HOST
	print str(err)
	print(str(s.close()))
	print str(s)
#**************************************************************************************
# If socket is null, exit
#**************************************************************************************
if s is None:
	print "Socket error while connecting"
	exit()
if s:
	try:
		try :
			line = s.recv(512)
			while (line != ""):
			
				print line #server message is output to console
				
				if line.find("No ident response") != -1:
					sUSERNICK(s, NICK)
				
				if line.find("PING :") != -1:
					pingrequest = re.search("PING :(.+)", line)
					s.sendall("PONG :" + pingrequest.group(1))
					s.sendall('USER ' +NICK + ' ' + NICK + ' ' + NICK + ' : ' + REALNAME + '\r\n')
					s.sendall('AUTH ' + NICK + ' ' + PASS + '\r\n')
					
				if line.find("001") != -1:
					s.sendall('JOIN #'+CHANNELINIT + "\r\n") #Joins default channel
					
				if line.split(':')[2] == NICK + " quitplz":
					s.sendall("PRIVMSG " + line.split(' ')[2] + " :Adios muchachos")
					s.sendall("QUIT")
					s.close()
					sys.exit(0)
				
				if line.find("Hello " + NICK) != -1:
					print("PRIVMSG " + line.split(' ')[2] + " :Hello! :) I am nex-bot <3")
					s.sendall("PRIVMSG " + line.split(' ')[2] + " :Hello! :) I am nex-bot <3")
				count = 1
				count = count + 1
				line = s.recv(512)		
			s.close()
			print "Exiting now"
			exit()
		except Exception, err:
			print "MY ERROR: " + str(err)
			s.close()
			sys.exit(0)
	except KeyboardInterrupt:
		print "Forced exit from user"
		if s:
			s.sendall("QUIT")
			s.close()
		sys.exit(0)