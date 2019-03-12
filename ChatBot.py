import socket
import random
import datetime
import requests
import select
import sys
import os
from bs4 import BeautifulSoup
s = socket.socket()
def send_usr(s1, s2):
	s.send(("PRIVMSG "+s2+" :"+s1).encode())
	return

def geturl(s):
	url = "https://www.youtube.com/results?search_query="+s
	request = requests.get(url)
	content = request.content
	soup = BeautifulSoup(content, "html.parser")
	collect = soup.select_one("div.yt-lockup-dismissable")
	if collect is None :
		return ("sorry i can't find any song!\r\n")
	link = collect.select_one("a.spf-link").get("href")
	return ("https://www.youtube.com"+link+"\r\n")

def pro(s):
	index = s.find("!")
	if index == -1:
		# send_usr("alive\n", "bot_b05902066")
		return 1, "", ""
	usr = s[1:s.find("!")]
	# print(usr)
	msg = s[s.rfind(":")+1:]
	return 0, usr, msg

	


s.connect((sys.argv[1], int(sys.argv[2])))

nickname = input("your nickname: ")
username = input("your username: ")
channelname = input("channel name: ")

s.send(('NICK '+nickname+'\n').encode())
s.send(('USER '+username+'\n').encode())
s.send(('JOIN '+channelname+'\n').encode())
s.send(('PRIVMSG '+channelname+' :I\'m '+nickname+'\n').encode())
mode = 0
const = ["Capricorn", "Aquarius", "Pisces", "Aries", "Taurus", "Gemini", "Cancer", "Leo", \
"Virgo", "Libra", "Scorpio", "Sagittarius"]
random.seed(datetime.datetime.now())
num = random.randint(1, 10)
game_list = {}
chat_person = ""

while(True):

	rlist = select.select([s, sys.stdin], [], [])[0]
	
	if sys.stdin in rlist:
		buf = sys.stdin.readline()
		sys.stderr.write("> ")
		sys.stderr.flush()
		if chat_person != "":
			# sys.stderr.write(buf)
			send_usr(buf, chat_person)

	if s in rlist:
		msg = s.recv(4096).decode()
	else:
		continue

	# print(msg)
	check, usr, msg = pro(msg)
	


	if check == 1 or usr == username:
		continue

	# print(usr, chat_person)

	if usr == chat_person :
		# print("is")
		op = msg.split()
		if len(op) is 0:
			continue
		sys.stderr.write("\r"+usr+": "+msg+"> ")
		if op[0] == "!bye":
			sys.stderr.write("\r==="+usr+" leaves===\r\n")
			chat_person = ""
			continue
		continue

	if usr not in game_list :
		op = msg.split()
		if len(op) == 0:
			continue
		if op[0] in const:
			send_usr("i don't care!\r\n", usr)
			continue
		if op[0] == "!guess":
			num = random.randint(1, 10)
			game_list[usr] = num
			send_usr("1~10?\r\n", usr)
			continue
		if op[0] == "!song":
			if len(op) < 2:
				send_usr("which song?\r\n", usr)
				continue
			send_usr(geturl(op[1]), usr)
			continue
		if op[0] == "!chat":
			if chat_person == "":
				sys.stderr.write("\r==="+usr+" wants to contact===\r\n> ")
				chat_person = usr
				continue
			if usr != chat_person :
				send_usr("bot is chatting with others, try later!\r\n", usr)
			continue
	else:
		op = msg.split()
		if len(op) == 0:
			continue
		try :
			get_num = int(op[0])
		except:
			# send_usr("bad guess, try again\n", usr)
			continue
		else:
			if get_num > game_list[usr] :
				send_usr("smaller than "+op[0]+"\r\n", usr)
			elif get_num < game_list[usr] :
				send_usr("bigger than "+op[0]+"\r\n", usr)
			else :
				send_usr("Get it!\r\n", usr)
				del game_list[usr]
		continue

s.close()