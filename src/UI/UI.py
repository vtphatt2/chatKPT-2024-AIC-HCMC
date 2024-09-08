from PyQt6 import QtCore, QtGui, QtWidgets
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1112, 665)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Set up textInputWindow and its widgets
        self.textInputWindow = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.textInputWindow.setGeometry(QtCore.QRect(20, 20, 281, 281))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(8)
        self.textInputWindow.setFont(font)
        self.textInputWindow.setObjectName("textInputWindow")
        self.textInput = QtWidgets.QPlainTextEdit(parent=self.textInputWindow)
        self.textInput.setGeometry(QtCore.QRect(10, 20, 256, 131))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(8)
        self.textInput.setFont(font)
        self.textInput.setObjectName("textInput")
        self.peopleNumber = QtWidgets.QSpinBox(parent=self.textInputWindow)
        self.peopleNumber.setGeometry(QtCore.QRect(70, 160, 42, 21))
        self.peopleNumber.setObjectName("peopleNumber")
        self.label = QtWidgets.QLabel(parent=self.textInputWindow)
        self.label.setGeometry(QtCore.QRect(10, 159, 47, 14))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.textInputWindow)
        self.label_2.setGeometry(QtCore.QRect(10, 200, 47, 14))
        self.label_2.setObjectName("label_2")
        self.maleNumber = QtWidgets.QSpinBox(parent=self.textInputWindow)
        self.maleNumber.setGeometry(QtCore.QRect(70, 200, 42, 21))
        self.maleNumber.setObjectName("maleNumber")
        self.label_3 = QtWidgets.QLabel(parent=self.textInputWindow)
        self.label_3.setGeometry(QtCore.QRect(10, 240, 47, 14))
        self.label_3.setObjectName("label_3")
        self.femaleNumber = QtWidgets.QSpinBox(parent=self.textInputWindow)
        self.femaleNumber.setGeometry(QtCore.QRect(70, 240, 42, 21))
        self.femaleNumber.setObjectName("femaleNumber")
        self.clearText = QtWidgets.QPushButton(parent=self.textInputWindow)
        self.clearText.setGeometry(QtCore.QRect(190, 160, 75, 41))
        self.clearText.setObjectName("clearText")
        self.clearNumber = QtWidgets.QPushButton(parent=self.textInputWindow)
        self.clearNumber.setGeometry(QtCore.QRect(190, 210, 75, 41))
        self.clearNumber.setObjectName("clearNumber")
        
        # Set up sketchInputWindow and its widgets
        self.sketchInputWindow = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.sketchInputWindow.setGeometry(QtCore.QRect(20, 310, 281, 271))
        self.sketchInputWindow.setObjectName("sketchInputWindow")
        self.graphicsView = QtWidgets.QGraphicsView(parent=self.sketchInputWindow)
        self.graphicsView.setGeometry(QtCore.QRect(10, 20, 256, 144))
        self.graphicsView.setObjectName("graphicsView")
        self.clearGraphic = QtWidgets.QPushButton(parent=self.sketchInputWindow)
        self.clearGraphic.setGeometry(QtCore.QRect(190, 170, 75, 41))
        self.clearGraphic.setObjectName("clearGraphic")
        self.loadGraphic = QtWidgets.QPushButton(parent=self.sketchInputWindow)
        self.loadGraphic.setGeometry(QtCore.QRect(190, 220, 75, 41))
        self.loadGraphic.setObjectName("loadGraphic")
        
        # Set up search and clearAll buttons
        self.search = QtWidgets.QPushButton(parent=self.centralwidget)
        self.search.setGeometry(QtCore.QRect(170, 590, 121, 41))
        self.search.setObjectName("search")
        self.clearAll = QtWidgets.QPushButton(parent=self.centralwidget)
        self.clearAll.setGeometry(QtCore.QRect(30, 590, 121, 41))
        self.clearAll.setObjectName("clearAll")
        
        # Set up scrollable grid layout
        self.scrollArea = QtWidgets.QScrollArea(parent=self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(310, 20, 791, 611))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 791, 611))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        
        self.loadImages()

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        
        # Connect buttons to event handlers
        self.clearText.clicked.connect(self.clear_text_content)
        self.clearNumber.clicked.connect(self.clear_spinbox_values)
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textInputWindow.setTitle(_translate("MainWindow", "Text Input"))
        self.label.setText(_translate("MainWindow", "Person"))
        self.label_2.setText(_translate("MainWindow", "Male"))
        self.label_3.setText(_translate("MainWindow", "Female"))
        self.clearText.setText(_translate("MainWindow", "Clear text"))
        self.clearNumber.setText(_translate("MainWindow", "Clear no."))
        self.sketchInputWindow.setTitle(_translate("MainWindow", "Sketch Input"))
        self.clearGraphic.setText(_translate("MainWindow", "Clear"))
        self.loadGraphic.setText(_translate("MainWindow", "Load"))
        self.search.setText(_translate("MainWindow", "Search"))
        self.clearAll.setText(_translate("MainWindow", "Clear all"))

    def loadImages(self):
        directory = "../../data/batch1/keyframes/keyframes_L01/L01_V001"
        for index, filename in enumerate(os.listdir(directory)):
            if filename.lower().endswith('.jpg'):
                image_path = os.path.join(directory, filename)
                pixmap = QtGui.QPixmap(image_path)
                image_label = QtWidgets.QLabel()
                image_label.setPixmap(pixmap.scaled(150, 150, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
                image_label.setFixedSize(150, 150)
                
                name_label = QtWidgets.QLabel(filename)
                
                overlay_layout = QtWidgets.QVBoxLayout()
                overlay_layout.setContentsMargins(0, 0, 0, 0)
                overlay_layout.addWidget(image_label)
                overlay_layout.addWidget(name_label, alignment=QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignRight)
                
                container = QtWidgets.QWidget()
                container.setLayout(overlay_layout)
                
                row = index // 5
                col = index % 5
                self.gridLayout.addWidget(container, row, col)
    
    # Event handler for Clear text button
    def clear_text_content(self):
        self.textInput.clear()

    # Event handler for Clear no. button
    def clear_spinbox_values(self):
        self.peopleNumber.setValue(0)
        self.maleNumber.setValue(0)
        self.femaleNumber.setValue(0)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
