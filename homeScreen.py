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

		self.bluetoothButton = QPushButton(constants.BLUETOOTH_PAGE_BUTTON_TEXT);
		self.bluetoothButton.setStyleSheet("font-size:24px;");
		self.bluetoothButton.clicked.connect(lambda: self.requestWork.emit(constants.BLUETOOTH_PAGE));

		self.requestButton = QPushButton(constants.REQUEST_PAGE_BUTTON_TEXT);
		self.requestButton.setStyleSheet("font-size:24px;");
		self.requestButton.clicked.connect(lambda: self.requestWork.emit(constants.REQUEST_PAGE));

		self.testServerConnectButton = QPushButton(constants.SERVER_CONNECT_CHECK_BUTTON_TEXT);
		self.testServerConnectButton.setStyleSheet("font-size:24px;");
		self.testServerConnectButton.clicked.connect(self.testServerConnect);
		self.layout.addWidget(self.testServerConnectButton);

		self.layout.addWidget(self.bluetoothButton);
		self.layout.addWidget(self.requestButton);
		self.setLayout(self.layout);

		self.connectedLabel = QLabel("");
		self.connectedLabel.setStyleSheet("font-size:24px;");
		self.layout.addWidget(self.connectedLabel);

		self.carStartLabel = QLabel(f"{constants.CAR_START_TEXT} : ");
		self.carStartLabel.setStyleSheet("font-size:24px;");
		self.layout.addWidget(self.carStartLabel);

		self.vehicleSpeedLabel = QLabel(f"{constants.VEHICLE_SPEED_TEXT} : ");
		self.vehicleSpeedLabel.setStyleSheet("font-size:24px;");
		self.layout.addWidget(self.vehicleSpeedLabel);

		self.doorLockLabel = QLabel(f"{constants.DOOR_LOCK_TEXT} : ");
		self.doorLockLabel.setStyleSheet("font-size:24px;");
		self.layout.addWidget(self.doorLockLabel);

		self.warningLabel = QLabel(f"{constants.WARNING_TEXT} : ");
		self.warningLabel.setStyleSheet("font-size:24px;");
		self.layout.addWidget(self.warningLabel);

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
		
			self.carStartLabel.setText(f"{constants.CAR_START_TEXT} : {carStart}");
			self.vehicleSpeedLabel.setText(f"{constants.VEHICLE_SPEED_TEXT} : {vehicleSpeed}");
			self.doorLockLabel.setText(f"{constants.DOOR_LOCK_TEXT} : {doorLock}");
			warningDetailText = "";
			if self.isHumanDetected():
				warningDetailText = constants.WARNING_HUMAN_DETECTED_TEXT;
			self.warningLabel.setText(f"{constants.WARNING_TEXT} : {warningDetailText}");
			if self.updateCount * constants.SENSOR_GET_DATA_CYCLE > constants.SEND_LOG_CYCLE :
				if self.serverConnect.sendLog(int(carStart), int(not doorLock), int(self.isHumanDetected()), vehicleSpeed, self.warningNumber()) :
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
		return True;
	
	def warningNumber(self):
		return 1;
if __name__ == '__main__':
	app = QApplication(sys.argv)
	homeScreen = HomeScreen(Obd2ClientService());
	homeScreen.show();
	sys.exit(app.exec_())