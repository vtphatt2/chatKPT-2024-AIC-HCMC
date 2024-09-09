from PyQt6 import QtCore, QtGui, QtWidgets
from glob import glob
import os


class Ui_MainWindow(object):

    def __init__(self):
        self.back_ground_task = BackgroundTask()
        self.back_ground_task.newQuery.connect(self.loadImages)
        self.back_ground_task.start()

    def save_text_query(self):
        text = self.textInput.toPlainText()
        save_path = r"D:\AIC 2024\chatKPT-2024-AIC-HCMC\query\pack-pretest\query.txt"
        with open(save_path, "w") as f:
            f.write(text)

    def addImage(self, path):
        self.loadImages(path)

    def setupUi(self, MainWindow, path):
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

        # Set up textInput and its widgets
        self.textInput = QtWidgets.QPlainTextEdit(parent=self.textInputWindow)
        self.textInput.setGeometry(QtCore.QRect(10, 20, 256, 131))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(8)
        self.textInput.setFont(font)
        self.textInput.setObjectName("textInput")

        # Set up peopleNumber
        self.peopleNumber = QtWidgets.QSpinBox(parent=self.textInputWindow)
        self.peopleNumber.setGeometry(QtCore.QRect(70, 160, 42, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.peopleNumber.sizePolicy().hasHeightForWidth())
        self.peopleNumber.setSizePolicy(sizePolicy)
        self.peopleNumber.setObjectName("peopleNumber")

        # Set up labels
        self.label = QtWidgets.QLabel(parent=self.textInputWindow)
        self.label.setGeometry(QtCore.QRect(10, 159, 47, 14))
        self.label.setObjectName("label")

        # Set up labels and spin
        self.label_2 = QtWidgets.QLabel(parent=self.textInputWindow)
        self.label_2.setGeometry(QtCore.QRect(10, 200, 47, 14))
        self.label_2.setObjectName("label_2")

        # Set up maleNumber
        self.maleNumber = QtWidgets.QSpinBox(parent=self.textInputWindow)
        self.maleNumber.setGeometry(QtCore.QRect(70, 200, 42, 21))
        self.maleNumber.setObjectName("maleNumber")

        # Set up label 3
        self.label_3 = QtWidgets.QLabel(parent=self.textInputWindow)
        self.label_3.setGeometry(QtCore.QRect(10, 240, 47, 14))
        self.label_3.setObjectName("label_3")

        # Set up femaleNumber
        self.femaleNumber = QtWidgets.QSpinBox(parent=self.textInputWindow)
        self.femaleNumber.setGeometry(QtCore.QRect(70, 240, 42, 21))
        self.femaleNumber.setObjectName("femaleNumber")

        # Set up clearText and clearNumber buttons
        self.clearText = QtWidgets.QPushButton(parent=self.textInputWindow)
        self.clearText.setGeometry(QtCore.QRect(190, 160, 75, 41))
        font = QtGui.QFont()
        font.setStrikeOut(False)
        self.clearText.setFont(font)
        self.clearText.setObjectName("clearText")

        # Set up clearNumber button
        self.clearNumber = QtWidgets.QPushButton(parent=self.textInputWindow)
        self.clearNumber.setGeometry(QtCore.QRect(190, 210, 75, 41))
        self.clearNumber.setObjectName("clearNumber")
        
        # Set up sketchInputWindow and its widgets
        self.sketchInputWindow = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.sketchInputWindow.setGeometry(QtCore.QRect(20, 310, 281, 271))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(8)
        self.sketchInputWindow.setFont(font)
        self.sketchInputWindow.setObjectName("sketchInputWindow")
        self.graphicsView = QtWidgets.QGraphicsView(parent=self.sketchInputWindow)
        self.graphicsView.setGeometry(QtCore.QRect(10, 20, 256, 144))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.graphicsView.setFont(font)
        self.graphicsView.setObjectName("graphicsView")
        self.clearGraphic = QtWidgets.QPushButton(parent=self.sketchInputWindow)
        self.clearGraphic.setGeometry(QtCore.QRect(190, 170, 75, 41))
        font = QtGui.QFont()
        font.setStrikeOut(False)
        self.clearGraphic.setFont(font)
        self.clearGraphic.setObjectName("clearGraphic")
        self.loadGraphic = QtWidgets.QPushButton(parent=self.sketchInputWindow)
        self.loadGraphic.setGeometry(QtCore.QRect(190, 220, 75, 41))
        font = QtGui.QFont()
        font.setStrikeOut(False)
        self.loadGraphic.setFont(font)
        self.loadGraphic.setObjectName("loadGraphic")
        
        # Set up search and clearAll buttons
        self.search = QtWidgets.QPushButton(parent=self.centralwidget)
        self.search.setGeometry(QtCore.QRect(170, 590, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(8)
        self.search.setFont(font)
        self.search.setObjectName("search")
        self.search.clicked.connect(lambda: self.save_text_query()) # Connect the button to the save_text function

        self.clearAll = QtWidgets.QPushButton(parent=self.centralwidget)
        self.clearAll.setGeometry(QtCore.QRect(30, 590, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(8)
        self.clearAll.setFont(font)
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
        
        self.loadImages(path)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textInputWindow.setTitle(_translate("MainWindow", "Text Input"))
        self.textInput.setPlainText(_translate("MainWindow", ""))
        self.label.setText(_translate("MainWindow", "People"))
        self.label_2.setText(_translate("MainWindow", "Male"))
        self.label_3.setText(_translate("MainWindow", "Female"))
        self.clearText.setText(_translate("MainWindow", "Clear text"))
        self.clearNumber.setText(_translate("MainWindow", "Clear no."))
        self.sketchInputWindow.setTitle(_translate("MainWindow", "Sketch Input"))
        self.clearGraphic.setText(_translate("MainWindow", "Clear"))
        self.loadGraphic.setText(_translate("MainWindow", "Load"))
        self.search.setText(_translate("MainWindow", "Search"))
        self.clearAll.setText(_translate("MainWindow", "Clear all"))

    def loadImages(self, path = None):
        
        self.clearLayout(self.gridLayout)   
        try:
            with open(path, "r") as file:
                image_paths = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            pass

        # Iterate over files in the directory
        for index, image_path in enumerate(image_paths):
            if image_path.lower().endswith('.jpg'):
                # Create a QLabel for each image
                pixmap = QtGui.QPixmap(image_path)
                image_label = QtWidgets.QLabel()
                image_label.setPixmap(pixmap.scaled(150, 150, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
                image_label.setFixedSize(150, 150)
                
                # Create a QLabel for the image name
                filename = os.path.basename(image_path)
                name_label = QtWidgets.QLabel(filename)
                
                # Create a QVBoxLayout to overlay the name on the image
                overlay_layout = QtWidgets.QVBoxLayout()
                overlay_layout.setContentsMargins(0, 0, 0, 0)
                overlay_layout.addWidget(image_label)
                overlay_layout.addWidget(name_label, alignment=QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignRight)
                
                # Create a QWidget to hold the layout and add it to the grid layout
                container = QtWidgets.QWidget()
                container.setLayout(overlay_layout)
                
                row = index // 5
                col = index % 5
                self.gridLayout.addWidget(container, row, col)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

class BackgroundTask(QtCore.QThread):
    newQuery = QtCore.pyqtSignal(str) # Signal to send new query to the model

    def run(self):
        base_dir = r"D:\AIC 2024\chatKPT-2024-AIC-HCMC\data\batch1\keyframes"
        with open("D:\AIC 2024\chatKPT-2024-AIC-HCMC\submission\output_keyframes.csv", "r") as f:
            lines = f.readlines()
            for line in lines:
                video, keyframes_id = line.strip().split(",")
                video_dir = f"keyframes_{video.split('_')[0]}"
                image_path = os.path.join(base_dir, video_dir, video, f"{video}_{keyframes_id}.jpg")
                
                # Store image_path to image_path.txt
                save_path = r"D:\AIC 2024\chatKPT-2024-AIC-HCMC\submission\image_path.txt"
                with open(save_path, "a") as file:
                    file.write(image_path + "\n")
                
            self.newQuery.emit(save_path)

def run_app(path = None):
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, path)
    MainWindow.show()

    background_task = BackgroundTask()
    background_task.start()

    try:
        app.exec()            
    except SystemExit:
        pass

if __name__ == "__main__":
    run_app()
