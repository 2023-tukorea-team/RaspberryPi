# -*- coding: euc-kr -*-
import sys;
import constants;
from obd2ClientService import *;
from serverConnect import *;
from loadingTextLabel import *;
from PyQt5.QtWidgets import *;
from PyQt5.QtCore import *;
from  PyQt5.QtGui import *;
from time import sleep;
from acceptDialog import *;

class BluetoothScreen(QWidget):
	requestWork = pyqtSignal(int);
	def __init__(self,  obd2ClientService):
		super().__init__();
		self.devices = [];
		self.layout = QVBoxLayout();

		width = self.width();
		height = self.height();
		self.backIcon = QIcon("back.png");
		self.backButton = QPushButton(self);
		self.backButton.setIcon(self.backIcon);
		self.backButton.setIconSize(QSize(width * 0.06, width * 0.06));
		self.backButton.setStyleSheet("border: none;");
		self.backButton.setGeometry(width * 0.02, height * 0.02, width * 0.06, width * 0.06);		
		self.backButton.clicked.connect(lambda: self.requestWork.emit(constants.HOME_PAGE));

		self.bluetoothGuideLabel = QLabel(constants.BLUETOOTH_GUIDE_TEXT);
		self.layout.addWidget(self.bluetoothGuideLabel);
		self.bluetoothGuideLabel.setStyleSheet("font-size:24px;");
		self.obd2ClientService = obd2ClientService;

		self.listView = QListView();
		self.layout.addWidget(self.listView);
		self.model = QStringListModel();
		self.listView.setModel(self.model);
		self.listView.setStyleSheet("font-size:24px;");
		self.selectedDevice = None;

		self.buttonLayout = QHBoxLayout();
		self.connectButton = QPushButton(constants.BLUETOOTH_CONNECT_TEXT, self);
		self.scanButton = QPushButton(constants.BLUETOOTH_SCAN_TEXT, self);

		self.buttonLayout.addWidget(self.connectButton);
		self.connectButton.setStyleSheet("font-size:24px;");
		self.connectButton.clicked.connect(self.connectButtonClicked);

		self.buttonLayout.addWidget(self.scanButton);
		self.scanButton.setStyleSheet("font-size:24px;");
		self.scanButton.clicked.connect(self.scanButtonClicked);

		self.layout.addLayout(self.buttonLayout);

		self.stateLabel = QLabel();
		self.layout.addWidget(self.stateLabel);
		self.setLayout(self.layout);
		self.resizeEvent(None);

	def setItems(self, items):
		self.model.setStringList(items);

	def showEvent(self,event):
		super().showEvent(event);
	
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

	def scanButtonClicked(self, event):			
		self.connectButton.setEnabled(False);
		self.connectButton.setStyleSheet("color: gray; font-size: 24px;");
		self.connectButton.update();

		self.scanButton.setEnabled(False);
		self.scanButton.setStyleSheet("color: gray; font-size: 24px;");
		self.scanButton.update();

		QApplication.processEvents();

		self.devices = self.obd2ClientService.scanDevices();
		self.connectButton.setEnabled(True);
		self.connectButton.setStyleSheet("color: black; font-size: 24px;");
		self.scanButton.setEnabled(True);
		self.scanButton.setStyleSheet("color: black; font-size: 24px;");

		print("scan 종료");
		tmp = [];
		for addr, name, _ in self.devices :
			tmp.append(name + " : " + addr);
		if len(self.devices) == 0 :
			tmp.append("검색된 장치가 없습니다.");
		self.setItems(tmp);
	
	def connectButtonClicked(self, event):
		self.selectedDevice = self.getSelectedDevice();
		if self.selectedDevice == None :
			dialog = AcceptDialog("선택된 장치가 없습니다");
			dialog.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
			dialog.exec_();
			return;
		print(self.selectedDevice[0]);
		print(constants.BLUETOOTH_PORT);
		self.obd2ClientService.makeConnect(self.selectedDevice[1], self.selectedDevice[0], constants.BLUETOOTH_PORT);
		if self.obd2ClientService.isConnected():
			dialog = AcceptDialog("장치 연결 성공");
			dialog.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
			dialog.exec_();
		else:
			dialog = AcceptDialog("장치 연결 실패");
			dialog.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
			dialog.exec_();
		pass;

	def getSelectedDevice(self):
		if len(self.devices) == 0:
			return None;
		selectedIndex = self.listView.selectedIndexes();
		if selectedIndex:
			index = selectedIndex[0].row();
			print(self.devices);
			print(index);
			return [self.devices[index][0], self.devices[index][1]];
		else :
			return None;

if __name__ == "__main__" :
	app = QApplication(sys.argv)
	bluetoothScreen = BluetoothScreen(Obd2ClientService());
	bluetoothScreen.show()
	sys.exit(app.exec_());