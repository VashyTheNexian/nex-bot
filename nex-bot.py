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
#auth pass: wPvw!lTnxZ


f = open('C:/Users/Hebron/nex-bot/settings.config')
text = f.read()
f.close()



HOST = re.search("HOST:(.+)", text).group(1) #'irc.quakenet.org' #The server the bot's going to connect to
print HOST
"""
PORT = 6667 #The connection port is usually 6667
NICK = 'nex-bot' #The bot's nickname
REALNAME = 'nex-bot'
PASS = 'wPvw!lTnxZ'
CHANNELINIT = 'siralim' #The default channel for the bot

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create the socket
s.connect((HOST, PORT)) #Connect to server



#**************************************************************************************
# After NICK, the server sends PING :<random number> to you, which has to be replied with 
# PONG :<same number>. Then you may send USER, the registration process is done 
# and raw 001 or an ERROR (klined, server full, etc.) is sent to you. The server also sends 
#PINGs in the same way with a certain interval, which have to be replied in the same way.
#**************************************************************************************
def sUSERNICK(s, NICK):
	IDENT = 'pybot'
	OWNER = 'Vashy' #The bot's owner's name
	s.send('NICK '+NICK + "\r\n") #Sends the nickname to the server


#**************************************************************************************
# This function handles the closing of the bot from the CLI using Ctrl+C
# It makes sure the socket gets closed
#**************************************************************************************
def signal_handler(signal, frame):
	print 'Now exiting because of Ctrl + C'
	s.close()
	sys.exit(0)
	
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
	"""