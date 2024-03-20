# -*- coding: euc-kr -*-
import sys;
import constants;
from obd2ClientService import *;
from startScreen import *;
from bluetoothScreen import *;
from homeScreen import *;
from requestScreen import *;
from PyQt5.QtWidgets import *;
from PyQt5.QtCore import *;
import paho.mqtt.client as mqtt;
import serial;
import threading;

class Main(QMainWindow):
	def __init__(self):
		super().__init__();
		self.obd2ClientService = Obd2ClientService();
		self.serverConnect = ServerConnect();
		self.setWindowState(Qt.WindowFullScreen)
		self.setWindowTitle("FullScreen");

		self.serial = serial.Serial('/dev/ttyS0', 9600);
		self.running = True;
		self.task = threading.Thread(target=self.uwbRecvTask);
		self.task.start();
		self.lock = threading.Lock();

		self.widgetList = [];
		self.stack = QStackedWidget();
		self.setCentralWidget(self.stack);

		self.widgetList.append(StartScreen(self.serverConnect));
		self.widgetList.append(HomeScreen(self.obd2ClientService, self.serverConnect, self.getUwbData));
		self.widgetList.append(RequestScreen(self.serverConnect));
		self.widgetList.append(BluetoothScreen(self.obd2ClientService));

		self.stack.addWidget(self.widgetList[constants.START_PAGE]);
		self.stack.addWidget(self.widgetList[constants.BLUETOOTH_PAGE]);
		self.stack.addWidget(self.widgetList[constants.REQUEST_PAGE]);
		self.stack.addWidget(self.widgetList[constants.HOME_PAGE]);

		self.widgetList[constants.START_PAGE].requestWork.connect(self.openScreen);
		self.widgetList[constants.BLUETOOTH_PAGE].requestWork.connect(self.openScreen);
		self.widgetList[constants.REQUEST_PAGE].requestWork.connect(self.openScreen);
		self.widgetList[constants.HOME_PAGE].requestWork.connect(self.openScreen);

		self.openScreen(constants.START_PAGE);

		self.mqttClient = mqtt.Client();
		self.mqttClient.on_connect = self.onConnect;
		self.mqttClient.username_pw_set(username=constants.MQTT_ID_TEXT, password=constants.MQTT_PWD_TEXT);
		self.mqttClient.connect(constants.SERVER_IP_TEXT, constants.MQTT_PORT);
		self.mqttClient.on_message = self.widgetList[constants.REQUEST_PAGE].addRequest;
		self.mqttClient.loop_start();

	def closeEvent(self, event):
		self.running = False;
		raise Exception("abc");
		self.task.join();

	def onConnect(self, client, userdata, flags, rc):
		print("Connected with result code " + str(rc));
		topic = constants.MQTT_TOPIC_LOOT_TEXT;
		topic += "/";
		topic += self.serverConnect.getMacAddress();
		print(topic);
		client.subscribe(topic);


	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.close();

	def openScreen(self, pageNum) :
		print(pageNum);
		print(self.widgetList[pageNum]);
		self.stack.setCurrentWidget(self.widgetList[pageNum]);
		return;

	def uwbRecvTask(self):
		while self.running :

			try:
				distance = self.serial.readline().decode('utf-8').strip();
				if len(distance) == 0 :
					continue;
				self.uwbData = distance;
				print("Received:", distance);
			except KeyboardInterrupt:
				self.serial.close();
				print("Serial communication closed.");
				break;
			except Exception:
				self.serial.close();
				self.serial = serial.Serial('/dev/ttyS0', 9600);
				pass;
		raise Exception("abc");
		self.serial.close();

	def getUwbData(self):
		with self.lock:
			ret = self.uwbData;
		return ret;
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	main = Main();
	main.show();
	sys.exit(app.exec_())