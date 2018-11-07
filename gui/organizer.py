# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'organizer.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import re
import os
import sys
import subprocess

class TextStream(QtCore.QObject):
    text = QtCore.pyqtSignal(str)
    def write(self, s):
        self.text.emit(str(s))

class Ui_MainWindow(object):    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1529, 658)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ad_text = QtWidgets.QTextEdit(self.centralwidget)
        self.ad_text.setGeometry(QtCore.QRect(10, 240, 311, 361))
        self.ad_text.setObjectName("ad_text")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 220, 151, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(330, 220, 151, 21))
        self.label_2.setObjectName("label_2")
        self.output_text = QtWidgets.QTextEdit(self.centralwidget)
        self.output_text.setGeometry(QtCore.QRect(660, 20, 851, 581))
        self.output_text.setObjectName("output_text")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(660, 0, 61, 20))
        self.label_3.setObjectName("label_3")
        self.run_button = QtWidgets.QPushButton(self.centralwidget)
        self.run_button.setGeometry(QtCore.QRect(470, 20, 161, 27))
        self.run_button.setObjectName("run_button")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 60, 631, 161))
        self.layoutWidget.setObjectName("layoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.layoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.ad_label = QtWidgets.QLabel(self.layoutWidget)
        self.ad_label.setObjectName("ad_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.ad_label)
        self.ad_opi_label = QtWidgets.QLabel(self.layoutWidget)
        self.ad_opi_label.setObjectName("ad_opi_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.ad_opi_label)
        self.ad_opi_line = QtWidgets.QLineEdit(self.layoutWidget)
        self.ad_opi_line.setObjectName("ad_opi_line")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.ad_opi_line)
        self.epics_label = QtWidgets.QLabel(self.layoutWidget)
        self.epics_label.setObjectName("epics_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.epics_label)
        self.epics_line = QtWidgets.QLineEdit(self.layoutWidget)
        self.epics_line.setObjectName("epics_line")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.epics_line)
        self.epics_opi_label = QtWidgets.QLabel(self.layoutWidget)
        self.epics_opi_label.setObjectName("epics_opi_label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.epics_opi_label)
        self.epics_opi_line = QtWidgets.QLineEdit(self.layoutWidget)
        self.epics_opi_line.setObjectName("epics_opi_line")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.epics_opi_line)
        self.css_label = QtWidgets.QLabel(self.layoutWidget)
        self.css_label.setObjectName("css_label")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.css_label)
        self.css_line = QtWidgets.QLineEdit(self.layoutWidget)
        self.css_line.setObjectName("css_line")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.css_line)
        self.ad_line = QtWidgets.QLineEdit(self.layoutWidget)
        self.ad_line.setObjectName("ad_line")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.ad_line)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 20, 441, 29))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.config_label = QtWidgets.QLabel(self.layoutWidget1)
        self.config_label.setObjectName("config_label")
        self.horizontalLayout.addWidget(self.config_label)
        self.config_line = QtWidgets.QLineEdit(self.layoutWidget1)
        self.config_line.setObjectName("config_line")
        self.horizontalLayout.addWidget(self.config_line)
        self.config_button = QtWidgets.QPushButton(self.layoutWidget1)
        self.config_button.setObjectName("config_button")
        self.horizontalLayout.addWidget(self.config_button)
        self.epics_text = QtWidgets.QTextEdit(self.centralwidget)
        self.epics_text.setGeometry(QtCore.QRect(330, 240, 311, 361))
        self.epics_text.setObjectName("epics_text")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1529, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.config_line.setReadOnly(True)
        self.ad_line.setReadOnly(True)
        self.ad_opi_line.setReadOnly(True)
        self.epics_line.setReadOnly(True)
        self.epics_opi_line.setReadOnly(True)
        self.css_line.setReadOnly(True)
        self.ad_text.setReadOnly(True)
        self.epics_text.setReadOnly(True)
        self.output_text.setReadOnly(True)

        self.config_button.clicked.connect(self.selectConfig)
        self.run_button.clicked.connect(self.organize)
        self.run_button.setEnabled(False)

        self.process = QtCore.QProcess(MainWindow)
        self.process.readyRead.connect(lambda: self.outputText(str(self.process.readAll(), 'utf-8')))
        self.process.started.connect(lambda: self.run_button.setEnabled(False))
        self.process.finished.connect(lambda: self.run_button.setEnabled(True))
        
        sys.stdout = TextStream(text=self.outputText)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "OPI Organizer"))
        self.label.setText(_translate("MainWindow", "AreaDetector modules"))
        self.label_2.setText(_translate("MainWindow", "EPICS modules"))
        self.label_3.setText(_translate("MainWindow", "Output"))
        self.run_button.setText(_translate("MainWindow", "Run"))
        self.ad_label.setText(_translate("MainWindow", "AreaDetector folder"))
        self.ad_opi_label.setText(_translate("MainWindow", "AreaDetector OPI folder"))
        self.epics_label.setText(_translate("MainWindow", "EPICS folder"))
        self.epics_opi_label.setText(_translate("MainWindow", "EPICS OPI folder"))
        self.css_label.setText(_translate("MainWindow", "CS-Studio executable"))
        self.config_label.setText(_translate("MainWindow", "Config file"))
        self.config_button.setText(_translate("MainWindow", "Choose file"))

        
    def outputText(self, text):
        cursor = self.output_text.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(text)
        self.output_text.ensureCursorVisible()

        
    def clearout(self):
        self.output_text.setPlainText("")

        
    def organize(self):
        self.clearout()
        print("Running...\n")
        os.chdir('..')
        platform = sys.platform
        if 'linux' in platform.lower():
            self.process.start('bash run.sh -f ' + self.config_line.text())
        elif 'win' in platform.lower():
            path = os.path.join(os.getcwd(), "run_windows.bat")
            self.process.start(path + ' -f ' + self.config_line.text())
        print("done")

        
    def selectConfig(self):
        self.config_line.setText("")
        self.ad_line.setText("")
        self.ad_opi_line.setText("")
        self.epics_line.setText("")
        self.epics_opi_line.setText("")
        self.css_line.setText("")
        self.ad_text.setPlainText("")
        self.epics_text.setPlainText("")
        self.clearout()
        self.run_button.setEnabled(False)
        config = QFileDialog.getOpenFileName()[0]
        if config != '':
            self.config_line.setText(config)
            self.parseConfig()

            
    def parseConfig(self):
        config = open(self.config_line.text())
        foundOPI_AD = foundOPI_EPICS = foundAD = foundEPICS = foundCSS = False
        # search for paths
        for line in config:
            if foundOPI_AD and foundOPI_EPICS and foundAD and foundEPICS and foundCSS:
                break
            if "#" in line:
                continue
            if not foundOPI_AD:
                match = self.search("AD_OPI_DIRECTORY : (.*)", line, True)
                if match is not None:
                    foundOPI_AD = True
                    self.ad_opi_line.setText(match)
                    continue
            if not foundAD:
                match = self.search("AD_DIRECTORY : (.*)", line, True)
                if match is not None:
                    foundAD = True
                    self.ad_line.setText(match)
                    continue
            if not foundOPI_EPICS:
                match = self.search("EPICS_OPI_DIRECTORY : (.*)", line, True)
                if match is not None:
                    foundOPI_EPICS = True
                    self.epics_opi_line.setText(match)
                    continue
            if not foundEPICS:
                match = self.search("EPICS_DIRECTORY : (.*)", line, True)
                if match is not None:
                    foundEPICS = True
                    self.epics_line.setText(match)
                    continue
            if not foundCSS:
                match = self.search("CSS_PATH : (.*)", line, False)
                if match is not None:
                    foundCSS = True
                    self.css_line.setText(match)
                    continue
        # only allow user to run scripts if they have given all the required input
        if foundAD and foundOPI_AD and foundEPICS and foundOPI_EPICS and foundCSS:
            print("Ready to run.")
            self.run_button.setEnabled(True)
        config.seek(0)
        # search for AD modules
        start = False
        for line in config:
            if '#' in line or line.strip() == "":
                continue
            if 'BEGIN_AD' in line:
                start = True
                continue
            if 'END_AD' in line:
                break
            if start is False:
                continue
            self.ad_text.setPlainText(self.ad_text.toPlainText() + line)
        config.seek(0)
        # seach for EPICS modules
        start = False
        for line in config:
            if '#' in line or line.strip() == "":
                continue
            if 'BEGIN_EPICS' in line:
                start = True
                continue
            if 'END_EPICS' in line:
                break
            if start is False:
                continue
            self.epics_text.setPlainText(self.epics_text.toPlainText() + line)

            
    def search(self, regex, line, isDir):
        search = re.search(regex, line)
        if search is not None:
            match = search.group(1)
            if isDir:
                if os.path.isdir(match):
                    return match
                print("Invalid path: " + match)
                return None
            else:
                return match
        return None


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

