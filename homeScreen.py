# -*- coding: euc-kr -*-
import sys;
import constants;
from obd2ClientService import *;
from serverConnect import *;
from loadingTextLabel import *;
from PyQt5.QtWidgets import *;
from PyQt5.QtCore import *;
from time import sleep;
from obd2ClientService import *;
from acceptDialog import *;

class HomeScreen(QWidget):
	requestWork = pyqtSignal(int);
	def __init__(self, obd2ClientService, serverConnect):
		super().__init__();
		self.layout = QVBoxLayout();
		self.loadingTextLabel = LoadingTextLabel(constants.SERVER_CONNECT_LOADING_TEXT);
		self.obd2ClientService = obd2ClientService;

		self.serverConnect = serverConnect;

		self.bluetoothButton = QPushButton("������� ���� ������");
		self.bluetoothButton.setStyleSheet("font-size:24px;");
		self.bluetoothButton.clicked.connect(lambda: self.requestWork.emit(constants.BLUETOOTH_PAGE));

		self.requestButton = QPushButton("��ȸ ���� ��û ������");
		self.requestButton.setStyleSheet("font-size:24px;");
		self.requestButton.clicked.connect(lambda: self.requestWork.emit(constants.REQUEST_PAGE));

		self.testServerConnectButton = QPushButton("���� ���� �׽�Ʈ");
		self.testServerConnectButton.setStyleSheet("font-size:24px;");
		self.testServerConnectButton.clicked.connect(self.testServerConnect);
		self.layout.addWidget(self.testServerConnectButton);

		self.layout.addWidget(self.bluetoothButton);
		self.layout.addWidget(self.requestButton);
		self.setLayout(self.layout);

		self.connectedLabel = QLabel("");
		self.connectedLabel.setStyleSheet("font-size:24px;");
		self.layout.addWidget(self.connectedLabel);

		self.carStartLabel = QLabel("�õ� : ");
		self.carStartLabel.setStyleSheet("font-size:24px;");
		self.layout.addWidget(self.carStartLabel);

		self.vehicleSpeedLabel = QLabel("�ӵ� : ");
		self.vehicleSpeedLabel.setStyleSheet("font-size:24px;");
		self.layout.addWidget(self.vehicleSpeedLabel);

		self.doorLockLabel = QLabel("�� ��� : ");
		self.doorLockLabel.setStyleSheet("font-size:24px;");
		self.layout.addWidget(self.doorLockLabel);

		self.updateTimer = QTimer(self);
		self.updateTimer.timeout.connect(self.update);
		self.updateTimer.start(100);

	def testServerConnect(self):
		if self.serverConnect.connectConfirm() :
			AcceptDialog("success").exec_();
		else :
			AcceptDialog("fail").exec_();
	def update(self):
		if self.obd2ClientService.isConnected() :
			self.connectedLabel.setText("obd2 Bluetooth Adapter : �����");

			carStart = None;
			try:
				carStart = self.obd2ClientService.getCarStart();
			except Exception as e:
				print(f"Recv Failed : {e}");
				return;

			vehicleSpeed = 0;
			try:
				vehicleSpeed = self.obd2ClientService.getVehicleSpeed();
			except Exception as e:
				print(f"Recv Failed : {e}");
				return;

			doorLock = None;
			try:
				doorLock = self.obd2ClientService.getDoorLock();
			except Exception as e:
				print(f"Recv Failed : {e}");
				return;
		
			self.carStartLabel.setText(f"�õ� : {carStart}");
			self.vehicleSpeedLabel.setText(f"�ӵ� : {vehicleSpeed}");
			self.doorLockLabel.setText(f"�� ��� : {doorLock}");
			if self.serverConnect.sendLog(int(carStart), int(not doorLock), 1, vehicleSpeed, 1) :
				print("send log Succeed");
			else :
				print("send log Failed");
				AcceptDialog("send log Failed").exec_();

		else :
			self.connectedLabel.setText("obd2 Bluetooth Adapter : ����Ǿ� ���� ����");
		pass;
	def showEvent(self, event):
		self.update();

if __name__ == '__main__':
	app = QApplication(sys.argv)
	homeScreen = HomeScreen(Obd2ClientService());
	homeScreen.show();
	sys.exit(app.exec_())