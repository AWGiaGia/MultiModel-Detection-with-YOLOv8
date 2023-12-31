# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'home_page.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(339, 327)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(22)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.image_annotation_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.image_annotation_pushButton.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.image_annotation_pushButton.setFont(font)
        self.image_annotation_pushButton.setStyleSheet("border:2px solid black;border-radius:10px;")
        self.image_annotation_pushButton.setObjectName("image_annotation_pushButton")
        self.verticalLayout.addWidget(self.image_annotation_pushButton)
        self.modal_fusion_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.modal_fusion_pushButton.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.modal_fusion_pushButton.setFont(font)
        self.modal_fusion_pushButton.setStyleSheet("border:2px solid black;border-radius:10px;")
        self.modal_fusion_pushButton.setObjectName("modal_fusion_pushButton")
        self.verticalLayout.addWidget(self.modal_fusion_pushButton)
        self.data_processing_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.data_processing_pushButton.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.data_processing_pushButton.setFont(font)
        self.data_processing_pushButton.setStyleSheet("border:2px solid black;border-radius:10px;")
        self.data_processing_pushButton.setObjectName("data_processing_pushButton")
        self.verticalLayout.addWidget(self.data_processing_pushButton)
        self.target_detection_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.target_detection_pushButton.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.target_detection_pushButton.setFont(font)
        self.target_detection_pushButton.setStyleSheet("border:2px solid black;border-radius:10px;")
        self.target_detection_pushButton.setObjectName("target_detection_pushButton")
        self.verticalLayout.addWidget(self.target_detection_pushButton)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "微光红外实时数据处理与目标检测系统"))
        self.label.setText(_translate("MainWindow", "微光红外实时数据处理\n"
"与目标检测系统"))
        self.image_annotation_pushButton.setText(_translate("MainWindow", "图像标注"))
        self.modal_fusion_pushButton.setText(_translate("MainWindow", "模态融合"))
        self.data_processing_pushButton.setText(_translate("MainWindow", "数据处理"))
        self.target_detection_pushButton.setText(_translate("MainWindow", "目标检测"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
