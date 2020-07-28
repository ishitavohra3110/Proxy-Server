import os,sys,random,time

if len(sys.argv) < 4:
	print "Syntax :: python2 client_endsystem.py <Client_port> <Proxy_port> <Server_port>"
	sys.exit(1)

Client_port = sys.argv[1]
Proxy_port = sys.argv[2]
Server_port = sys.argv[3]
method = 0
while True:
	x = int(random.random()*3)+1

	data = "%d.data" % (x)
	method = (method+1)%2
	# method = 2
	if method == 1:
		y = "GET"
		os.system("curl --request %s --proxy 127.0.0.1:%s --local-port %s  'http://www.fortune.com'  --proxy-user %s" %(y,Proxy_port,Client_port,'vani:pass1'))
	else:
		y = "POST"
		print data 
		os.system("curl --request %s --proxy 127.0.0.1:%s --local-port %s  127.0.0.1:%s/%s  --proxy-user %s" %(y,Proxy_port,Client_port,Server_port,data,'vani:pass1'))
	time.sleep(10)