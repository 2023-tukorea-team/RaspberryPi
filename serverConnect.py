import requests;
import constants;
import query;
import netifaces;

class ServerConnect:
	def __init__(self):
		self.serverAddress = "http://" + constants.SERVER_IP + ":" + constants.SERVER_PORT + "/" ;
		self.macAddress = netifaces.ifaddresses('eth0')[netifaces.AF_LINK][0]['addr'];

	def connectConfirm(self):
		url = self.serverAddress + query.CHECK_ID;
		data = { 'id' : self.macAddress };
		response = requests.post(url, json=data);
		if response.status_code == 200:
			result = response.json()
			print(result);
			if result['result'] == False and result['entry'] == False :
				print("server DB Error");
				return False;
			return True;
		else :
			return  False;

if __name__ == "__main__" :
	serverConnect = ServerConnect();
	print(serverConnect.connectConfirm());
