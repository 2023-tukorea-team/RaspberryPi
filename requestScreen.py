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

		self.acceptGuideLabel = QLabel(constants.ACCEPT_GUIDE_TEXT);
		self.layout.addWidget(self.acceptGuideLabel);
		self.acceptGuideLabel.setStyleSheet("font-size:36px;");

		self.listView = QListView();
		self.layout.addWidget(self.listView);
		self.model = QStringListModel();
		self.listView.setModel(self.model);
		self.listView.setStyleSheet("font-size:36px;");
		self.selectedRequest = None;

		self.deleteButton = QPushButton(constants.DELETE_TEXT);
		self.deleteButton.setStyleSheet("font-size:36px;");
		self.deleteButton.clicked.connect(self.deleteButtonClicked);

		self.layout.addWidget(self.deleteButton);

		self.requestList = [];

	def deleteButtonClicked(self):
		selectedIndex = self.getSelectedRequestIndex();
		if selectedIndex == -1 :
			return;
		self.selectedRequest =  self.requestList[selectedIndex];
		print(self.selectedRequest[0]);
		self.requestList.pop(selectedIndex);
		self.setItems(self.requestList);
	
	def getSelectedRequestIndex(self):
		if len(self.requestList) == 0:
			return -1;
		selectedIndex = self.listView.selectedIndexes();
		if selectedIndex:
			index = selectedIndex[0].row();
			print(self.requestList);
			print(index)
			return index;
		else :
			return -1;

	def openHomeScreen(self):
		self.reqeustWork.emit();

	def setItems(self, items):
		self.model.setStringList(items);

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

	def addRequest(self, client, userData, message):
		recvMsg = message.payload.decode('utf-8');
		print("Received message:", recvMsg);
		items = recvMsg.strip("{}").split(", ");
		data = {};
		for item in items:
			key, value = item.split("=");
			data[key.strip()] = value.strip();
		id = data["id"];
		code = data["code"];
		string = constants.CONNECT_REQUEST_USER_ID_TEXT + " : " + id + "\n" + constants.CODE_TEXT + " : " + code;
		print(string);
		self.requestList.append(string);
		self.setItems(self.requestList);

if __name__ ==  '__main__':
	app = QApplication(sys.argv)
	requestScreen = RequestScreen(ServerConnect());
	requestScreen.show();
	sys.exit(app.exec_())