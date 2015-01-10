import socks
import socket
import requests
import stem.process

PORT = 7000

# DNS resolution
def getaddrinfo(*args):
	return [(socket.AF_INET, socks.SOCK_STREAM, 6, "", (args[0], args[1]))]

def query(url, countryCode):
	print requests.get(url).text,"from exit node in",countryCode

def make_request_thru_tor(countryCode, url):
	print "Connecting to tor..."
	socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", PORT)
	socket.socket = socks.socksocket

	socks.getaddrinfo = getaddrinfo

	print "Starting to configure tor"
	# make sure that a secondary tor process is not running!
	try:
		tor_config = stem.process.launch_tor_with_config(
			config = {"SocksPort" : str(PORT), "ExitNodes" : "{" + countryCode + "}"})
	except:
		tor_config.kill()

	print "Querying",url
	query(url, countryCode)

	tor_config.kill()

def main():
	make_request_thru_tor("ru", "http://my.kirby.org/accounts/login")
	#make_request_thru_tor("ru", "http://my-ip.heroku.com")

if __name__ == '__main__' : main()