# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'compare.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import requests
from PyQt5.QtCore import QEventLoop, QTimer
from bs4 import BeautifulSoup
import datetime


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1638, 861)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.inputbox = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.inputbox.setGeometry(QtCore.QRect(0, 0, 1081, 381))
        self.inputbox.setObjectName("inputbox")
        self.startbutton = QtWidgets.QPushButton(self.centralwidget)
        self.startbutton.setGeometry(QtCore.QRect(0, 380, 1361, 51))
        self.startbutton.setStyleSheet("font: 75 12pt \"MS Shell Dlg 2\";")
        self.startbutton.setObjectName("startbutton")
        self.startbutton.clicked.connect(self.start)
        self.outputbox = QtWidgets.QTextBrowser(self.centralwidget)
        self.outputbox.setGeometry(QtCore.QRect(0, 430, 1631, 401))
        self.outputbox.setObjectName("outputbox")
        self.notificationbox = QtWidgets.QTextBrowser(self.centralwidget)
        self.notificationbox.setGeometry(QtCore.QRect(1090, 0, 541, 381))
        self.notificationbox.setObjectName("notificationbox")
        self.dismissbutton = QtWidgets.QPushButton(self.centralwidget)
        self.dismissbutton.setGeometry(QtCore.QRect(1370, 380, 261, 51))
        self.dismissbutton.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.dismissbutton.setObjectName("dismissbutton")
        self.dismissbutton.clicked.connect(self.dismiss)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Stock Checker"))
        self.startbutton.setText(_translate("MainWindow", "Start"))
        self.dismissbutton.setText(_translate("MainWindow", "Dismiss all notifications"))

    def start(self):
        prev_output =[]
        # prev_output =[['B07WF8H189', '55.99', '', 'Not Available', ''], ['B01N94HLTS', '20', '', 'Not Available', '']]
        while True:
            print(prev_output)
            input_data = self.inputbox.toPlainText()
            input_list = input_data.split("\n\n")
            input_2d_list=[]
            for i in range(0,len(input_list)):
                if input_list[i]=="":
                    continue
                input_2d_list.append(input_list[i].split("\n"))

            output_2d_list=[]
            now = datetime.datetime.now()
            print(now.strftime("%Y-%m-%d %H:%M:%S"))
            for i in range(0,len(input_2d_list)):
                print("getting data from internet "+str(i))
                try:
                    output_element = []
                    product_code = input_2d_list[i][0]
                    amazon_link = input_2d_list[i][1].split('"')[1]
                    amazon_cutoff_price = input_2d_list[i][1].split('"')[2].split("-")[1]
                    currys_link = input_2d_list[i][2].split('"')[1]
                    currys_cutoff_price = input_2d_list[i][2].split('"')[2].split("-")[1]

                    my_header = {
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
                    }
                    res = requests.get(amazon_link,headers=my_header)
                    soup = BeautifulSoup(res.text, features="html.parser")
                    buybox = soup.find("span", {"id": "price_inside_buybox"})
                    output_element.append(product_code)
                    if(buybox==None):
                        output_element.append("Not Available")
                        output_element.append("")
                    else:
                        output_element.append(buybox.text[2:-1])
                        if(float(buybox.text[2:])<float(amazon_cutoff_price)):
                            output_element.append(" Lower than expect")
                        else:
                            output_element.append("")

                    res = requests.get(currys_link, headers=my_header)
                    soup = BeautifulSoup(res.text, features="html.parser")
                    buybox = soup.find("strong", {"data-key": "current-price"})
                    if (buybox == None):
                        output_element.append("Not Available")
                        output_element.append("")
                    else:
                        output_element.append(buybox.text[1:])
                        if (float(buybox.text[1:]) < float(currys_cutoff_price)):
                            output_element.append(" Lower than expect")
                        else:
                            output_element.append("")

                    output_2d_list.append(output_element)
                except:
                    continue
            self.outputbox.clear()

            for i in range(0,len(output_2d_list)):
                self.outputbox.append(output_2d_list[i][0])
                self.outputbox.append("Amazon : "+output_2d_list[i][1]+output_2d_list[i][2])
                self.outputbox.append("Currys : "+output_2d_list[i][3]+output_2d_list[i][4]+"\n")

            notifications = []
            if(prev_output!=output_2d_list):
                if(len(prev_output)==len(output_2d_list)):
                    for i in range(0,len(prev_output)):
                        if (prev_output[i][1] != output_2d_list[i][1]):
                            notifications.append(
                                "Product " + output_2d_list[i][0] + " in Amazon, value changed from: " + prev_output[i][
                                    1] + " to: " + output_2d_list[i][1] + " " + output_2d_list[i][2])
                        if (prev_output[i][3] != output_2d_list[i][3]):
                            notifications.append(
                                "Product " + output_2d_list[i][0] + " in Currys, value changed from: " + prev_output[i][
                                    3] + " to: " + output_2d_list[i][3] + " " + output_2d_list[i][4])

            if(len(notifications)!=0):
                self.notificationbox.append(now.strftime("%Y-%m-%d %H:%M:%S"))
                for i in range(0, len(notifications)):
                    self.notificationbox.append(notifications[i])


            prev_output = output_2d_list
            print("start sleeping")
            loop = QEventLoop()
            QTimer.singleShot(60000, loop.quit)
            loop.exec_()
            print("end sleeping")

    def dismiss(self):
        print("dismissing notifications")
        self.notificationbox.clear()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
