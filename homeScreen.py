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
	def __init__(self, obd2ClientService, serverConnect, getUwbData):
		super().__init__();
		self.layout = QVBoxLayout();
		self.loadingTextLabel = LoadingTextLabel(constants.SERVER_CONNECT_LOADING_TEXT);
		self.obd2ClientService = obd2ClientService;

		self.serverConnect = serverConnect;
		self.getUwbData = getUwbData;

		self.bluetoothButton = QPushButton(constants.BLUETOOTH_PAGE_BUTTON_TEXT);
		self.bluetoothButton.setStyleSheet("font-size:36px;");
		self.bluetoothButton.clicked.connect(lambda: self.requestWork.emit(constants.BLUETOOTH_PAGE));

		self.requestButton = QPushButton(constants.REQUEST_PAGE_BUTTON_TEXT);
		self.requestButton.setStyleSheet("font-size:36px;");
		self.requestButton.clicked.connect(lambda: self.requestWork.emit(constants.REQUEST_PAGE));

		self.testServerConnectButton = QPushButton(constants.SERVER_CONNECT_CHECK_BUTTON_TEXT);
		self.testServerConnectButton.setStyleSheet("font-size:36px;");
		self.testServerConnectButton.clicked.connect(self.testServerConnect);
		self.layout.addWidget(self.testServerConnectButton);

		self.layout.addWidget(self.bluetoothButton);
		self.layout.addWidget(self.requestButton);
		self.setLayout(self.layout);

		self.connectedLabel = QLabel("");
		self.connectedLabel.setStyleSheet("font-size:36px;");
		self.layout.addWidget(self.connectedLabel);

		self.carStartLabel = QLabel(f"{constants.CAR_START_TEXT} : ");
		self.carStartLabel.setStyleSheet("font-size:36px;");
		self.layout.addWidget(self.carStartLabel);

		self.vehicleSpeedLabel = QLabel(f"{constants.VEHICLE_SPEED_TEXT} : ");
		self.vehicleSpeedLabel.setStyleSheet("font-size:36px;");
		self.layout.addWidget(self.vehicleSpeedLabel);

		self.doorLockLabel = QLabel(f"{constants.DOOR_LOCK_TEXT} : ");
		self.doorLockLabel.setStyleSheet("font-size:36px;");
		self.layout.addWidget(self.doorLockLabel);

		self.warningLabel = QLabel(f"{constants.WARNING_TEXT} : ");
		self.warningLabel.setStyleSheet("font-size:36px;");
		self.layout.addWidget(self.warningLabel);

		self.uwbLabel = QLabel(f"{constants.UWB_TEXT} : ");
		self.uwbLabel.setStyleSheet("font-size:36px;");
		self.layout.addWidget(self.uwbLabel);


		self.updateTimer = QTimer(self);
		self.updateTimer.timeout.connect(self.update);
		self.updateTimer.start(100);

		self.updateCount = 0;	
		self.failedDialogExist = False;

	def testServerConnect(self):
		if self.serverConnect.connectConfirm() :
			AcceptDialog("success").exec_();
		else :
			AcceptDialog("fail").exec_();
	def update(self):
		self.updateCount += 1;
		if self.obd2ClientService.isConnected() :
			self.connectedLabel.setText(constants.OBD2_CONNECTED_TEXT);

			self.carStart = None;
			try:
				self.carStart = self.obd2ClientService.getCarStart();
			except Exception as e:
				print(f"Recv Failed : {e}");
				return;

			self.vehicleSpeed = 0;
			try:
				self.vehicleSpeed = self.obd2ClientService.getVehicleSpeed();
			except Exception as e:
				print(f"Recv Failed : {e}");
				return;

			self.doorLock = None;
			try:
				self.doorLock = self.obd2ClientService.getDoorLock();
			except Exception as e:
				print(f"Recv Failed : {e}");
				return;
		
			self.carStartLabel.setText(f"{constants.CAR_START_TEXT} : {self.carStart}");
			self.vehicleSpeedLabel.setText(f"{constants.VEHICLE_SPEED_TEXT} : {self.vehicleSpeed}");
			self.doorLockLabel.setText(f"{constants.DOOR_LOCK_TEXT} : {self.doorLock}");
			self.uwbData = self.getUwbData();
			self.uwbLabel.setText(f"{constants.UWB_TEXT} : {self.uwbData}");
			warningDetailText = "";
			if self.warningNumber() != 0:
				warningDetailText = constants.WARNING_HUMAN_DETECTED_TEXT;
			self.warningLabel.setText(f"{constants.WARNING_TEXT} : {warningDetailText}");
			if self.updateCount * constants.SENSOR_GET_DATA_CYCLE > constants.SEND_LOG_CYCLE :
				if self.serverConnect.sendLog(int(self.carStart), int(not self.doorLock), int(self.isHumanDetected()), self.vehicleSpeed, self.warningNumber()) :
					print("send log Succeed");
				else :
					print("send log Failed");
				self.updateCount = 0;

		else :
			self.connectedLabel.setText(constants.OBD2_NOT_CONNECTED_TEXT);
		pass;
	def showEvent(self, event):
		self.update();

	def isHumanDetected(self):
		if self.uwbData > constants.HUMAN_EXIST_VALUE :
			return True;
		return False;
	
	def warningNumber(self):
		if int(self.carStart) ==0 and int(self.doorLock) == 1 and self.isHumanDetected() :
			return 1;
		return 0;

	def setUwbData(self, uwbData):
		self.uwbData = uwbData;
if __name__ == '__main__':
	app = QApplication(sys.argv)
	homeScreen = HomeScreen(Obd2ClientService(), ServerConnect(), lambda : 0);
	homeScreen.show();
	sys.exit(app.exec_())