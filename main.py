# -*- coding: euc-kr -*-
import sys;
from startScreen import *;
from bluetoothScreen import *;
from PyQt5.QtWidgets import *;
from PyQt5.QtCore import *;

class Main(QMainWindow):
	def __init__(self):
		super().__init__();
		self.setWindowState(Qt.WindowFullScreen)
		self.setWindowTitle("FullScreen");
		self.stack = QStackedWidget();
		self.setCentralWidget(self.stack);
		self.startScreen = StartScreen();
		self.stack.addWidget(self.startScreen);
		self.bluetoothScreen = BluetoothScreen();
		self.stack.addWidget(self.bluetoothScreen);
		self.openStartScreen();
		self.startScreen.requestWork.connect(self.openBluetoothScreen);

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.close();

	def openStartScreen(self):
		self.stack.setCurrentWidget(self.startScreen);

	def openBluetoothScreen(self):
		self.stack.setCurrentWidget(self.bluetoothScreen);
		pass;
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	main = Main();
	main.show();
	sys.exit(app.exec_())