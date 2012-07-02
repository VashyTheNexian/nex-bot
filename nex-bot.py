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
import datetime
#**************************************************************************************
# After NICK, the server sends PING :<random number> to you, which has to be replied with 
# PONG :<same number>. Then you may send USER, the registration process is done 
# and raw 001 or an ERROR (klined, server full, etc.) is sent to you. The server also sends 
#PINGs in the same way with a certain interval, which have to be replied in the same way.
#**************************************************************************************
def USERNICK(s, NICK):
	s.send('NICK '+NICK + "\r\n")
	
def PONG(s, line):
	pingrequest = re.search("PING :(.+)", line)
	print ('Sending: PONG : ' + pingrequest.group(1))
	s.sendall('PONG ' + pingrequest.group(1) + '\r\n')
	
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
	f = s.makefile()
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
	
#**************************************************************************************
# Bot execution
#**************************************************************************************
if s:
	try:
		try :
			line = f.readline().rstrip()
			while (line != ""):
				print line #server message is output to console
				
				if len(line.split(':')) >= 3:
					user = re.search(':(.+)!.+', line)
					if user is not None:
						user = user.group(1)
					channel = line.split(' ')[2]
					
				if line.find("No ident response") != -1:
					USERNICK(s, NICK)
				
				elif line.find("PING :") != -1:
					PONG(s, line)
					s.send('USER ' +NICK + ' ' + NICK + ' ' + NICK + ' : ' + REALNAME + '\r\n')
					s.send('AUTH ' + NICK + ' ' + PASS + '\r\n')
					
				elif line.find("001") != -1:
					s.send('JOIN #'+CHANNELINIT + "\r\n") #Joins default channel
					
				elif line.find(NICK + ' quitplz') != -1:
					if len(line.split(':')) >= 3 and line.split(':')[2] == NICK + " quitplz":
						#user = re.search(':(.+)!.+', line).group(1)
						if (user == 'Vashy'):
							channel = line.split(' ')[2]
							s.send("PRIVMSG " + channel + " :Adios muchachos\r\n")
							s.send("QUIT")
							s.close()
							sys.exit(0)
				elif line.find(NICK + ' rejoinplz') != -1:
					if len(line.split(':')) >= 3 and line.split(':')[2] == NICK + ' rejoinplz':
						#user = re.search(':
						if (user == 'Vashy'):
							s.sendall('QUIT \r\n')
							s.connect((HOST, PORT))
							f = s.makefile()
				#:Vashy!~Vash@173.168.202.248 PRIVMSG #siralim :nex-bot quitplz
				elif line.find("Hello " + NICK) != -1:
					channel = line.split(' ')[2]
					user = re.search(':(.+)!.+', line).group(1)
					s.sendall("PRIVMSG " + channel + " :Hello, " + user + "\r\n")
					
				elif len(line.split(':')) > 2:
					if line.split(':')[2] == NICK + ' servertimeplz':
						channel = line.split(' ')[2]
						user = re.search(':(.+)!.+', line).group(1)
						now = datetime.datetime.now()
						s.sendall("PRIVMSG " + channel + ' :' + user + ': Server time: ' + str(now)[:19] + ' \r\n')
				line = f.readline().rstrip()	
			s.close()
			print "Exiting now"
			exit()
		except Exception, err:
			print "MY ERROR: " + str(err)
			s.sendall("QUIT \r\n")
			s.close()
			sys.exit(0)
	except KeyboardInterrupt:
		print "Forced exit from user"
		if s:
			s.sendall("QUIT \r\n")
			s.close()
		sys.exit(0)