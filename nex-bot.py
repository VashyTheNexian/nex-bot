#!/usr/bin/python 
#**************************************************************************************
# VashyTheNexian
# Project start date - 06/22/2012
# 
# IRC Bot written in Python found example at: http://www.osix.net/modules/article/?id=780
#
#**************************************************************************************
import sys
import socket
import string

HOST = 'irc.quakenet.org' #The server the bot's going to connect to
PORT = 6667 #The connection port is usually 6667
NICK = 'nex-bot' #The bot's nickname
IDENT = 'pybot'
REALNAME = 'nex-bot'
OWNER = 'Vashy' #The bot's owner's name
CHANNELINIT = '#siralim' #The default channel for the bot
readbuffer = '' #Here we store all the messages from the server

s = socket.socket() #Create the socket
s.connect((HOST, PORT)) #Connect to server
s.send('NICK '+NICK) #Sends the nickname to the server
s.send('USER ' +NICK + ' ' + NICK + ' ' + NICK + ' : ' + REALNAME)
s.send('JOIN #'+CHANNELINIT) #Joins default channel

if s is None:
	print "Socket error while connecting"
	exit()
	
try :
	line = s.recv(512)
	while (line != None): 
		if line != None:
			print line #server message is output to screen
		else :
			s.close()
			break
		line = s.recv(512)
		
	exit()
except Exception, err:
	print "ERROR: " + str(err)
	s.close()
	exit()