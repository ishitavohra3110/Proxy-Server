import os,sys,thread,socket,datetime
from basicauth import encode

Blacklist = []
bfile = open("blacklist.txt","rb")
Blacklist = bfile.read()
Blacklist =  Blacklist.split('\n')
# print Blacklist
admins = {
	'vani'
}
admins_password = {
	'pass1'
}
username = {
	'vani',
	'ishita',
}
password = {
	'pass1',
	'pass2',
}
value = []
admin_value = []

for (i,j) in zip(username,password):
	# print i,j
	value.append(str(encode(i,j)))

for (i,j) in zip(admins,admins_password):
	# print i,j
	admin_value.append(str(encode(i,j)))

target_host = "www.google.com"
path = './cache'
url_present = {}
cached_mtime = {}
my_str = "Cache-Control"
comp = "no-store"

def main():
	Client_list = []
	for i in range(20000,20100):
		Client_list.append(int(i))

	try:
		
		proxy_s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		# print proxy_s
		# print "Print"
		# if proxy_s==-1:
		# 	print "Unable to create the socket! Try Again"
		proxy_s.bind(("", 20100))
		proxy_s.listen(10)

	except socket.error, (value,message):
		# if proxy_s:
		proxy_s.close()
		print message
		sys.exit(1)

	while(True):
		client1, add = proxy_s.accept()
		client1.send("Thank You\n")
		print "Client Request Received from"
		print add

		if int(add[1]) in Client_list: 
			try:
				thread.start_new_thread(request_rev, (client1,add))
			except Exception as e:
				print e
		else:
			print "Not Inside IIIT"
			client1.close();

def add_url(url1):
	if not (url1 in url_present):
		url_present[url1]= {}
		url_present[url1]["seconds"] = []
	date1 = datetime.datetime.now()
	sec = date1.hour*60+date1.minute*60+date1.second
	m = url_present[url1]
	m["seconds"].append(sec)
	# print m
	# print url_present

def check_for_cache(url1):
	if not (url1 in url_present):
		add_url(url1)
		return False
	elif len(url_present[url1]["seconds"])<3:
		# print len(url_present[url1]["seconds"])
		add_url(url1)
	sz = len(url_present[url1]["seconds"])
	# print sz
	if sz!=3:
		return False
	if sz==3:
		cur = url_present[url1]
		first = cur["seconds"][0]
		last = cur["seconds"][2]
		# print first
		# print last
		if first-last<=300:
			return True
		else:
			del url_present[url1]["seconds"][0]
			return False
def check_for_space():
	cnt = 0;
	for x in os.listdir('./cache'):
		cnt = cnt+1
	# print cnt
	if cnt>=3:
		return False
	else:
		return True 

def get_space(url):
	min1 = 10000000000
	for x in os.listdir('./cache'):
		cur_dir = './cache/'+x
		time1 = os.path.getmtime(cur_dir)
		if min1 > time1:
			min1 = time1
			file = cur_dir
	os.remove(file)
	url1 = url.replace("/","+++")
	del url_present[url1]
def add_to_cache(cache_file,message,client1,sock):
	f = open(cache_file,"w+")
	while 1:
		if len(message)>0:
			client1.send(message)
			f.write(message)
			message = sock.recv(1024)
		else:
			break
	f.close()
def get_file_from_cache(cache_file,client1):
	f = open(cache_file,"rb")
 	get_data = f.read(1024)
 	while 1:
 		# print get_data
 		if len(get_data)>0:
 			client1.send(get_data)
 			get_data = f.read(1024)
 		else:
 			break
 	f.close()
def check_for_if_modified(url1,file):
	cur_mtime = os.path.getmtime(file)
	prev_mtime = cached_mtime[url1]
	# print prev_mtime
	# print cur_mtime
	if cur_mtime == prev_mtime:
		return 304#not modified
	else:
		return 200#modified
def can_it_be_cached(message):
	# x = message.split("\n")
	for i in range(len(message)):
		ft = i
		sd = i+13
		if sd>len(message):
			break
		substr = message[i:i+13]
		if substr == my_str:
			# print "Yipee"
			# print ft
			# print sd
			i+=13
			for i in range(len(message)):
				ft = i
				sd = i+8
				new_str = message[ft:sd]
				# print new_str
				if new_str==comp:
					return 0
	return 1

def get_method(url,client,request,client1,add):
	# print "GET"
	try:
		sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 		sock.connect((url,client))
 		sock.send(request)

 		message = sock.recv(1024)
 		# print message

 		flag = 0;
 		string = './cache/'
 		
 		x = url
 		# print x
 		url1 = x.replace("/","+++")
 		# print url1
 		cache_file = string+url1
 		print "CACHE FILE: "+ cache_file
 		checker = check_for_cache(url1)
 		# print checker
 		space = check_for_space()
 		# print os.listdir('./cache')
 		cached = 0
 		
 		for x in os.listdir('./cache'):
 			# print x
 			if x == url1: 				
 				flag = 1
 				cached = 1
 				break
 		
 		if cached:
 			valid_cache = can_it_be_cached(message)
 			if not valid_cache:
 				cached = 0
 			modify_stat = check_for_if_modified(url1,cache_file)
 			if modify_stat == 304:
 				flag = 1
 			else:
 				flag = 0
 				checker = 1
 		
 		if flag:#return cached file
 			get_file_from_cache(cache_file,client1)
 			print "message came from cache"
 		else:#either should be cached or no caching is required
 			if checker:#if it will be cached now
 				if not space:
 					get_space(url)
 					print "removed one cached file"
 				add_to_cache(cache_file,message,client1,sock)
 				cached_mtime[url1] = os.path.getmtime(cache_file)
 				print "Added to Cache"
 			else:
 				print "Message didn't come from cache"
 				while 1:
					if len(message) > 0:
						client1.send(message)
						message = sock.recv(1024)
					else:
						break

		sock.close()
		client1.close()
		# print "Done"

	except socket.error, (value,message):
		if sock:
			sock.close()
		if client1:
			client1.close()
		print "IN except\n"
		print message
		sys.exit(1)

def post_method(url,client,request,client1):
	try:
		send_req = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
		send_req.connect((url, client))
		send_req.send(request)
		while 1:
			outcome = send_req.recv(1024)
			# print outcome
			if len(outcome) > 0:
				client1.send(outcome)
			else:
				break

		send_req.close()
		client1.close()
		return

	except socket.error, (value,message):
		if send_req:
			send_req.close()
		if client1:
			client1.close()
		print message
		sys.exit(1)


def request_rev(client1,add):
	authenticated = False
	admin = False


	request = client1.recv(1024)
	req = request
	request = request.split('\n')
	lines = request
	request = request[0]

	keys = []
	values = []
	for i in lines:
		temp = i.split(':')
		temp1 = temp[0]
		temp2 = temp[1:]
		keys.append(temp1)
		values.append(temp2)

	if 'Proxy-Authorization' in keys:
		auth = keys.index('Proxy-Authorization')
		if auth != -1:
			check = str(values[auth][0].replace(' ',''))
			check = str(check.replace('\r',''))

			for i in value:
				i = str(i.replace(' ',''))
				if check == i:
					authenticated = True

			for i in admin_value:
				i = str(i.replace(' ',''))
				# print check
				# print i
				if check == i:
					admin = True

	# print admin

	if authenticated:
		print "User Request Authenticated"
		client1.send("User authenticated\n")

		url = request.split(' ')
		method = url[0]
		url = url[1]

		# print method

		a = url.find("://")
		if a!=-1:
			url = url[a+3:]

		p = url.find(':')

		b = url.find("/")
		
		if b == -1:
			b = len(url)

		if p ==-1 or b < p:
			client = 80
			url = url[:b]
		else:
			client = int((url[(p+1):b]))
			# client = int((url[(p+1):])[:b-p-1])
			url = url[:p]

		# print url + ':' + str(client)
		Blocked = False

		if admin == False:
			for i in Blacklist:
				if str(url + ':' + str(client)) == str(i):
					Blocked = True
		
		if Blocked == False:
			if method == "GET":
				get_method(url,client,req,client1,add)
			else:
				post_method(url,client,req,client1)
		else:
			print "Blocked"
			client1.send("Site Blocked")
			client1.close()

	else:
		print "User Request Not Authenticated"
		client1.send("User Not authenticated\n")
		client1.close()
		sys.exit(1)


if __name__ == '__main__':
	main()
