# -*- coding: euc-kr -*-
import sys;
import constants;
from serverConnect import *;
from obd2ClientService import *;
from startScreen import *;
from bluetoothScreen import *;
from homeScreen import *;
from PyQt5.QtWidgets import *;
from PyQt5.QtCore import *;

class RequestScreen(QWidget):
	requestWork = pyqtSignal(int);
	def __init__(self, serverConnect):
		super().__init__();
		self.layout = QVBoxLayout();
		self.setLayout(self.layout);

		width = self.width();
		height = self.height();
		self.backIcon = QIcon("back.png");
		self.backButton = QPushButton(self);
		self.backButton.setIcon(self.backIcon);
		self.backButton.setIconSize(QSize(width * 0.06, width * 0.06));
		self.backButton.setStyleSheet("border: none;");
		self.backButton.setGeometry(width * 0.02, height * 0.02, width * 0.06, width * 0.06);		
		self.backButton.clicked.connect(lambda: self.requestWork.emit(constants.HOME_PAGE));

		self.label = QLabel("requestPage");
		self.layout.addWidget(self.label);
	def openHomeScreen(self):
		self.reqeustWork.emit();

	def resizeEvent(self, event):
		width = self.width();
		height = self.height();
		leftMargin = width * 0.1;
		topMargin = height * 0.1;
		rightMargin = width * 0.1;
		bottomMargin = height * 0.1;
		self.layout.setContentsMargins(leftMargin, topMargin, rightMargin, bottomMargin);
		self.backButton.setIconSize(QSize(width * 0.06, width * 0.06));
		self.backButton.setStyleSheet("border: none;");
		self.backButton.setGeometry(width * 0.02, height * 0.02, width * 0.06, width * 0.06);

if __name__ ==  '__main__':
	app = QApplication(sys.argv)
	requestScreen = RequestScreen(ServerConnect());
	requestScreen.show();
	sys.exit(app.exec_())