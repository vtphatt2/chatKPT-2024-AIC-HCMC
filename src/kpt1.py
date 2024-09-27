import sys
import os
import csv
import torch
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QScreen
from PyQt6.QtWidgets import QFileDialog
from sklearn.metrics.pairwise import cosine_similarity
#import fiftyone as fo
#from submission import submission, calculate_keyframe_id, getImageInformation, organizeOutput

class ImageWindow(QtWidgets.QWidget):
    def __init__(self, image_path):
        super().__init__()
        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, 1668, 1533)
        self.showFullScreen()
        
        splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)
        left_side_layout = QtWidgets.QVBoxLayout()
        left_side_widget = QtWidgets.QWidget()
        left_side_widget.setLayout(left_side_layout)
        
        self.selectedImageWindow = QtWidgets.QGroupBox(parent=left_side_widget)
        self.selectedImageWindow.setObjectName("selectedImageWindow")
        self.selectedImageWindow.setGeometry(self.rect())
        
        pixmap = QtGui.QPixmap(image_path)
        self.selectedImage = QtWidgets.QLabel(parent=self.selectedImageWindow)
        self.selectedImage.setGeometry(QtCore.QRect(10, 20, 400, 300))
        self.selectedImage.setPixmap(pixmap.scaled(400, 300, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        self.selectedImage.setObjectName("selectedImage")
   
        self.imageInfoWindow = QtWidgets.QGroupBox(parent=left_side_widget)
        self.imageInfoWindow.setObjectName("imageInfoWindow")
        self.imageInfoLayout = QtWidgets.QVBoxLayout(self.imageInfoWindow)
        
        left_side_layout.addWidget(self.selectedImageWindow)
        left_side_layout.addWidget(self.imageInfoWindow)
        
        self.scrollArea = QtWidgets.QScrollArea(parent=self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 791, 611))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        
        splitter.addWidget(left_side_widget)
        splitter.addWidget(self.scrollArea)
        splitter.setSizes([6, 4]) 
        
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)
        
        # self.loadKeyframes(image_path)
        # self.load_metadata(image_path)
        # self.retranslateUi(image_path)

    def retranslateUi(self, image_path):
        _translate = QtCore.QCoreApplication.translate
        # subdir, file_name = os.path.split(image_path)
        # subdir = os.path.basename(subdir)
        # selected_image_title = f"{subdir}/{file_name}"
        self.selectedImageWindow.setTitle(_translate("ImageWindow", "Selected Image"))
        self.imageInfoWindow.setTitle(_translate("ImageWindow", "Image Information"))

    def loadKeyframes(self, image_path):
        keyframe_paths = []
        directory = os.path.dirname(image_path)
        base_name = os.path.basename(image_path)
        base_number = int(os.path.splitext(base_name)[0])
    
        for i in range(base_number - 10, base_number + 11):
            keyframe_path = os.path.join(directory, f"{i}.jpg")
            if os.path.exists(keyframe_path):
                keyframe_paths.append(keyframe_path)
    
        for i in reversed(range(self.gridLayout.count())): 
            widget_to_remove = self.gridLayout.itemAt(i).widget()
            self.gridLayout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        for index, filename in enumerate(keyframe_paths):
            if filename.lower().endswith('.jpg'):
                pixmap = QtGui.QPixmap(filename)
            
                image_label = QtWidgets.QLabel()
                image_label.setPixmap(pixmap.scaled(150, 150, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
                image_label.setFixedSize(150, 150)

                subdir, file_name = os.path.split(filename)
                subdir = os.path.basename(subdir)
                name_label = QtWidgets.QLabel(f"{subdir}/{file_name}")

                overlay_layout = QtWidgets.QVBoxLayout()
                overlay_layout.setContentsMargins(0, 0, 0, 0)
                overlay_layout.addWidget(image_label)
                overlay_layout.addWidget(name_label, alignment=QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignRight)
                
                overlay_widget = QtWidgets.QWidget()
                overlay_widget.setLayout(overlay_layout)
            
                row = index // 5
                col = index % 5
                self.gridLayout.addWidget(overlay_widget, row, col)

    def load_metadata(self, image_path):
        publish_date, watch_url = getImageInformation(image_path)
        self.clear_layout(self.imageInfoLayout)
    
        metadata = {
            'Publish Date': publish_date,
            'Watch URL': watch_url
        }

        vbox = QtWidgets.QVBoxLayout()
        for key, value in metadata.items():
            if key == 'Watch URL':
                label = QtWidgets.QLabel(f'<a href="{value}">{key}: {value}</a>')
                label.setOpenExternalLinks(True)
            else:
                label = QtWidgets.QLabel(f"{key}: {value}")
            vbox.addWidget(label)
        self.imageInfoLayout.addLayout(vbox)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):        
        # get size of the screen
        screen = QtWidgets.QApplication.primaryScreen()
        size = screen.size()
        width, height = size.width(), size.height() - 100

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(width, height)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # set up Suggest obejct window
        self.suggestObjectWindow = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.suggestObjectWindow.setGeometry(QtCore.QRect(20, 20, int(width/8)-40, height-50))
        self.suggestObjectWindow.setObjectName("suggestObjectWindow")
        self.suggestObjectWindow.setTitle("Suggest Object")

        self.suggestObjectTextEdit = QtWidgets.QPlainTextEdit(parent=self.suggestObjectWindow)
        self.suggestObjectTextEdit.setGeometry(QtCore.QRect(10, 20, int(width/8)-60, height-80))
        self.suggestObjectTextEdit.setObjectName("suggestObjectTextEdit")
        self.suggestObjectTextEdit.setReadOnly(True)
        
        # Set up textInputWindow and its widgets
        self.textInputWindow = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.textInputWindow.setGeometry(QtCore.QRect(int(width/8)-20, 20, 2*int(width/8)-40, int(height/2)))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(8)
        self.textInputWindow.setFont(font)
        self.textInputWindow.setObjectName("textInputWindow")
        self.textInput = QtWidgets.QPlainTextEdit(parent=self.textInputWindow)
        self.textInput.setGeometry(QtCore.QRect(10, 10, 2*int(width/8)-60, int(height/4)-40))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(8)
        self.textInput.setFont(font)
        self.textInput.setObjectName("textInput")
        
        # Add Object Input label and text input
        self.objectInputLabel = QtWidgets.QLabel(parent=self.textInputWindow)
        self.objectInputLabel.setGeometry(QtCore.QRect(10,int(height/4)-30, 100, 20))
        self.objectInputLabel.setObjectName("objectInputLabel")
        self.objectInput = QtWidgets.QPlainTextEdit(parent=self.textInputWindow)
        self.objectInput.setGeometry(QtCore.QRect(10,int(height/4)-10, 2*int(width/16)-20 , int(height/4)))
        self.objectInput.setObjectName("objectInput")
        self.objectInput.textChanged.connect(self.handle_object_input)

        # Set up Search OR and Search OB buttons
        self.searchOR = QtWidgets.QPushButton(parent=self.textInputWindow)
        self.searchOR.setGeometry(QtCore.QRect(230, 180, 100, 41))
        self.searchOR.setObjectName("searchOR")
        self.searchOB = QtWidgets.QPushButton(parent=self.textInputWindow)
        self.searchOB.setGeometry(QtCore.QRect(230, 230, 100, 41))
        self.searchOB.setObjectName("searchOB")
        
        # Set up sketchInputWindow and its widgets
        self.sketchInputWindow = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.sketchInputWindow.setGeometry(QtCore.QRect(int(width/8)-20, int(height/2)+20 , 2*int(width/8)-40, int(height/2)-50))
        self.sketchInputWindow.setObjectName("sketchInputWindow")
        self.graphicsView = QtWidgets.QGraphicsView(parent=self.sketchInputWindow)
        self.graphicsView.setGeometry(QtCore.QRect(10, 20, 2*int(width/8)-60, 190))
        self.graphicsView.setObjectName("graphicsView")
        self.clearGraphic = QtWidgets.QPushButton(parent=self.sketchInputWindow)
        self.clearGraphic.setGeometry(QtCore.QRect(250, 220, 75, 41))
        self.clearGraphic.setObjectName("clearGraphic")
        self.loadGraphic = QtWidgets.QPushButton(parent=self.sketchInputWindow)
        self.loadGraphic.setGeometry(QtCore.QRect(150, 220, 75, 41))
        self.loadGraphic.setObjectName("loadGraphic")

        # Set up search and clearAll buttons
        self.search = QtWidgets.QPushButton(parent=self.centralwidget)
        self.search.setGeometry(QtCore.QRect(int(width/8) +20, height-80, 121, 41))
        self.search.setObjectName("search")
        self.clearAll = QtWidgets.QPushButton(parent=self.centralwidget)
        self.clearAll.setGeometry(QtCore.QRect(int(width/8)+180, height-80, 121, 41))
        self.clearAll.setObjectName("clearAll")

        # Set up scrollable grid layout
        self.scrollArea = QtWidgets.QScrollArea(parent=self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(3*int(width/8)-50, 20, 5*int(width/8)+20, height - 50))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 791, 611))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        
        #self.loadImages()

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        
        # Connect buttons to event handlers
        # self.clearGraphic.clicked.connect(self.clear_graphic_content)
        # self.clearAll.clicked.connect(self.clear_all_content)
        # self.loadGraphic.clicked.connect(self.load_graphic_image)
        # self.search.clicked.connect(self.handle_search)
        # self.searchOR.clicked.connect(self.handle_searchOR)
        # self.searchOB.clicked.connect(self.handle_searchOB)

        # Set up scene for graphicsView
        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self.scene)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textInputWindow.setTitle(_translate("MainWindow", "Text Input"))
        self.objectInputLabel.setText(_translate("MainWindow", "Object Input"))
        self.searchOR.setText(_translate("MainWindow", "Search OR"))
        self.searchOB.setText(_translate("MainWindow", "Search OB"))
        self.sketchInputWindow.setTitle(_translate("MainWindow", "Sketch Input"))
        self.clearGraphic.setText(_translate("MainWindow", "Clear"))
        self.loadGraphic.setText(_translate("MainWindow", "Load"))
        self.search.setText(_translate("MainWindow", "Search"))
        self.clearAll.setText(_translate("MainWindow", "Clear all"))

    def loadImages(self, image_result_path=None):
        if image_result_path is None:
            directory = "../data/batch1/keyframes/keyframes_L01/L01_V001"
            image_paths = [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith('.jpg')]
        else:
            with open(image_result_path, 'r') as file:
                image_paths = [line.strip() for line in file if line.strip().lower().endswith('.jpg')]

        for index, filename in enumerate(image_paths):
            if filename.lower().endswith('.jpg'):
                pixmap = QtGui.QPixmap(filename)
                
                image_label = QtWidgets.QLabel()
                image_label.setPixmap(pixmap.scaled(150, 150, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
                image_label.setFixedSize(150, 150)
                
                # Add click event to open image in new window
                image_label.mousePressEvent = lambda event, img_path=filename: self.show_image_in_window(img_path)
                
                # infor image
                subdir, file_name = os.path.split(filename)
                subdir = os.path.basename(subdir)

                name_label = QtWidgets.QLabel(f"{subdir}/{file_name}")
                
                overlay_layout = QtWidgets.QVBoxLayout()
                overlay_layout.setContentsMargins(0, 0, 0, 0)
                overlay_layout.addWidget(image_label)
                overlay_layout.addWidget(name_label, alignment=QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignRight)
                
                container = QtWidgets.QWidget()
                container.setLayout(overlay_layout)
                
                row = index // 5
                col = index % 5
                self.gridLayout.addWidget(container, row, col)
                
    def show_image_in_window(self, image_path):
        self.image_window = ImageWindow(image_path)
        self.image_window.show()
    
    def clear_text_content(self):
        self.textInput.clear()

    def clear_graphic_content(self):
        self.scene.clear()

    def clear_all_content(self):
        self.clear_text_content()
        self.clear_graphic_content()

    def load_graphic_image(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Open Image File", "", 
                                                "Images (*.png *.xpm *.jpg);;All Files (*)")
        
        if file_path:
            pixmap = QtGui.QPixmap(file_path)
            
            if not pixmap.isNull():
                self.scene.clear()
                scaled_pixmap = pixmap.scaled(self.graphicsView.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
                
                self.scene.addPixmap(scaled_pixmap)
                self.graphicsView.setScene(self.scene)
                self.graphicsView.fitInView(self.scene.itemsBoundingRect(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            else:
                print("Error loading the image!")

    def get_video_frame_id(self, path):
        with open(path, 'r') as file:
            lines = file.reader()
            for line in lines:
                video, frame_id = line.split(',')
                return video, frame_id
            
    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clear_layout(child.layout())
         
    def handle_search(self):
        text_query = self.textInput.toPlainText()
        csv_file = "output.csv"

        subqueries = text_query.split('/') if '/' in text_query else [text_query]
        is_subquery = '/' in text_query

        for subquery in subqueries:
            subquery = subquery.strip()
            dataset_submission = submission(subquery, 500, csv_file, is_subquery)
    
        keyframe_paths = calculate_keyframe_id(csv_file)

        # Clear the existing layout
        self.clear_layout(self.gridLayout)

        # load images from image_result_path.txt and put to loadImages
        self.loadImages("image_result_path.txt")

    def handle_searchOR(self):
        # Implement the logic for Search OR
        pass

    def handle_searchOB(self):
        # Implement the logic for Search OB
        pass

    def handle_object_input(self, predefined_text=None):
        if predefined_text is not None:
            input_text = predefined_text
        else:
            input_text = self.objectInput.toPlainText()
        print(f"Object Input: {input_text}")

def run_app(path = None):
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    try:
        app.exec()            
    except SystemExit:
        pass

if __name__ == "__main__":
    run_app()