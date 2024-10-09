import json,os,time,sys,requests
from urllib.parse import unquote, parse_qs, urlparse
def banner():
	os.system("clear")
	os.system("lolcat banner.txt")
def genAuthToken(query_string):
	decoded_query = unquote(query_string)
	parsed_query = parse_qs(decoded_query)
	userPayload=  decoded_query.split("https://ffabrika.com/#tgWebAppData=")[1].split("&tgWebAppVersion")[0]
	url = "https://api.ffabrika.com/api/v1/auth/login-telegram"
	data = '{"webAppData":{"payload":"' +userPayload+ '"}}'
	headers ={'Content-Type':'application/json'}
	response = requests.post(url,data=data,headers=headers)
	return response.cookies.get_dict()['acc_uid']
def profile(token):
	url = "https://api.ffabrika.com/api/v1/profile"
	headers ={'Content-Type':'application/json','Cookie':'acc_uid='+token}
	response= requests.get(url,headers=headers)
	return response.json()
def autoTap(token):
	url ="https://api.ffabrika.com/api/v1/scores"
	headers ={'Content-Type':'application/json','Cookie':'acc_uid='+token}
	data = '{"count":250}'
	response = requests.post(url, data=data,headers=headers)
	return response.json()
def activateBooster(token):
	url = "https://api.ffabrika.com/api/v1/energies/recovery"
	headers ={'Content-Type':'application/json','Cookie':'acc_uid='+token}
	response= requests.post(url,headers=headers)
	return response.json()
def info(query_string):
	datas = profile(genAuthToken(query_string))
	info =f'''\033[1;93m
Name: {datas["data"]["firstName"]} {datas["data"]["lastName"]}
Username: {datas["data"]["username"]}
Score: {datas["data"]["score"]["total"]}
Energy: {datas["data"]["energy"]["balance"]}
Recovery Booster: {datas["data"]["energy"]["currentRecoveryLimit"]}\033[1;97m
'''
	print(info)	
def wait(min):
	for remaining in range(min*60, 0, -1):
		mins, secs = divmod(remaining, 60)
		print("\033[1;96m",end="")
		text = f"{mins:02}:{secs:02}"
		sys.stdout.write(text)
		sys.stdout.flush()
		time.sleep(1)
		sys.stdout.write("\b" * len(text))
		
def infinite(query_string):
		os.system("clear")
		banner()
		info(query_string)
		token = genAuthToken(query_string)
		datas = profile(token)
		energy, booster = datas["data"]["energy"]["balance"],datas["data"]["energy"]["currentRecoveryLimit"]
		if energy < 20:
			wait(10)
		else:
			for i in range(500):
				token = genAuthToken(query_string)
				tap = autoTap(token)				
				text =  "Total: "+str(tap["data"]["score"]["balance"])
				sys.stdout.write(text)
				sys.stdout.flush()
				time.sleep(1)
				sys.stdout.write("\b" * len(text))
				if tap["data"]["energy"]["balance"] <10:
					infinite(query_string)
				else:
					pass
def option():
	op='''\033[1;92m
[1] Infinate Click
[2] Normal Click
'''
	print(op)		
def main(query_string):
		os.system("clear")
		banner()
		info(query_string)
		token = genAuthToken(query_string)
		datas = profile(token)
		energy, booster = datas["data"]["energy"]["balance"],datas["data"]["energy"]["currentRecoveryLimit"]
		if energy < 20:
			if booster!=0:
				conUseRec = str(input("\033[1;97mEnergy Low.\nUse Booster [Y/n]  ")).lower().replace(" ","")
				if conUseRec=="yes" or conUseRec=="y":
					token = genAuthToken(query_string)
					act = activateBooster(token)
					if act["statusCode"] ==201:
						print("Booster Activated..")
						for i in range(500):
							token = genAuthToken(query_string)
							tap = autoTap(token)
							text = "Total: "+str(tap["data"]["score"]["balance"])
							sys.stdout.write(text)
							sys.stdout.flush()
							time.sleep(1)
							sys.stdout.write("\b" * len(text))
							if tap["data"]["energy"]["balance"] <10:
								main(query_string)
							else:
								pass
					if act["message"] =="Recover energy is not available at the current point of time":
						print("\033[1;91mBoost Unavailable Right Now.")
						sys.exit()
				else:
					confirmRec = str(input("\033[1;97mWait 10 min for recover Energy?[Y/n] ")).lower().replace(" ","")
					if confirmRec == "yes" or confirmRec == "y":
						wait(10)
						main(query_string)
					else:
						sys.exit()
			else:
				confirmRec = str(input("\033[1;97mWait 10 min for recover Energy?[Y/n] ")).lower().replace(" ","")
				if confirmRec == "yes" or confirmRec == "y":
					wait(10)
					main(query_string)
				else:
					sys.exit()
		else:
			for i in range(500):
				token = genAuthToken(query_string)
				tap = autoTap(token)				
				text =  "Total: "+str(tap["data"]["score"]["balance"])
				sys.stdout.write(text)
				sys.stdout.flush()
				time.sleep(1)
				sys.stdout.write("\b" * len(text))
				if tap["data"]["energy"]["balance"] <10:
					main(query_string)
				else:
					pass
while True:
	banner()
	query_string = str(input("\033[1;96m\n\n[>] Enter Url: \033[1;97m"))
	time.sleep(1)
	urlmain = urlparse(query_string).netloc
	if urlmain == "ffabrika.com":
		os.system("clear")
		banner()
		option()
		op = str(input("\033[1;96m[>] Choose a option: \033[1;97m")).lower().replace(" ","")
		if op =="1" or op =="a":
			infinite(query_string)
		elif op == "2" or op=="b":
			main(query_string)
		break
	else:
		print("\033[1;91mPlease Enter Valid URL. ")
		time.sleep(3)