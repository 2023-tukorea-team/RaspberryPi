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

class Main(QMainWindow):
	def __init__(self):
		super().__init__();
		self.obd2ClientService = Obd2ClientService();
		self.serverConnect = ServerConnect();
		self.setWindowState(Qt.WindowFullScreen)
		self.setWindowTitle("FullScreen");

		self.widgetList = [];
		self.stack = QStackedWidget();
		self.setCentralWidget(self.stack);

		self.widgetList.append(StartScreen(self.serverConnect));
		self.widgetList.append(HomeScreen(self.obd2ClientService, self.serverConnect));
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

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.close();

	def openScreen(self, pageNum) :
		print(pageNum);
		print(self.widgetList[pageNum]);
		self.stack.setCurrentWidget(self.widgetList[pageNum]);
		return;
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	main = Main();
	main.show();
	sys.exit(app.exec_())