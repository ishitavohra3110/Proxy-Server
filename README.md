Computer Networks Assignment-2 
Proxy-Server
RollNo. - 20171179
	- 20171054


- Threaded Proxy Server: Multiple clients are handled by the server. For each client a new Thread is created

- Cache: Caching is done when you issue a request 3 times in 5 minutes.Maximum cache size is 3.Use of If-Since-Modified and Cache-control has been done to handle the whether the request has been modified since the last time it was cached and whether or not you have to cache a particular directory 

- Blacklisting: Some domains listed in the blacklist.txt are blocked that is they are not access by any user except some admin user

- Authorziation:Basic Access Authentication is used to encode the user-name and password that is matched with the encoded version of user name and password in proxy-server.

- If any user outside the network access he/she is rejected



- To run:
 -- python proxy_server1.py 
 -- python client_endsystem.py <CLIENT_PORT> <PROXY_PORT> <SERVER_PORT>
 -- python server.py <SERVER PORT> 
 -- server.py is present in the server folder
