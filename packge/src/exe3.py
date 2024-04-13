from TM_find_page import find_gri_pages
from TM_agent_getindex import get_index
from TM_extract_text import extract_text_from_pages
from TM_agent import get_draft
from Indextranslate import translate
import json
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Listbox, Toplevel
import threading
import json
import time
import sys
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QWidget, QInputDialog, QMessageBox, QFileDialog, QPlainTextEdit, QVBoxLayout)
# import logo1_rc

class GRIApp(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"GRI Draft Generator")
        MainWindow.resize(1027, 693)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(-10, 0, 1051, 631))
        self.label.setStyleSheet(u"background-color:rgb(255, 217, 102)")
        self.label_pic = QLabel(self.centralwidget)
        self.label_pic.setObjectName(u"label_pic")
        self.label_pic.setGeometry(QRect(400, 220, 241, 91))
        pixmap = QPixmap("./logo1.png")
        self.label_pic.setPixmap(pixmap)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(350, 320, 351, 61))
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.clicked.connect(self.select_pdf)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(200, 400, 671, 91))
        font1 = QFont()
        font1.setPointSize(15)
        self.pushButton.setFont(font1)
        self.pushButton.setStyleSheet(u"")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1027, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
        self.pdf_path = None
        self.raw_data = None
        self.index_list = []
        self.key = None  # key 속성을 추가합니다.      
        self.request_key()  #
    # setupUi

    def request_key(self):
    # 사용자로부터 키를 입력받는 메서드입니다.
        key, ok_pressed = QInputDialog.getText(None, "Input", "Please enter the key:")
        if ok_pressed:
            self.key = key
            if not self.key:
                QMessageBox.warning(self, "Warning", "The key is required to proceed.")
                self.request_key()  # 유효한 키를 받을 때까지 재요청합니다

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"GRI Draft Generator", None))
        self.label.setText("")
        self.label_pic.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\uc804\uae30 \ubcf4\uace0\uc11c\ub97c \ucca8\ubd80\ud574\uc8fc\uc138\uc694", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PDF \ud30c\uc77c\uc744 \ucca8\ubd80\ud574\uc8fc\uc138\uc694", None))
        self.raw_data_window.plainTextEdit.setPlaceholderText(QCoreApplication.translate("Form", u"\ub0b4\uc6a9\uc744 \uc785\ub825\ud574\uc8fc\uc138\uc694", None))
        self.raw_data_window.label_3.setText(QCoreApplication.translate("Form", u"\ud074\ub77c\uc774\uc5b8\ud2b8 \uc778\ud130\ubdf0, \uace0\uac1d\uc0ac \uc131\uacfc\uc790\ub8cc \ub4f1 Raw Data\ub97c \uc785\ub825\ud574\uc8fc\uc138\uc694!", None))
    # retranslateUi
    # retranslateUi

    def select_pdf(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.pdf_path, _ = QFileDialog.getOpenFileName(self.centralwidget, "Select PDF", "", "PDF files (*.pdf)", options=options)
        if self.pdf_path:
            QMessageBox.information(self, "PDF Selected", f"Selected PDF: {self.pdf_path}")
            self.prompt_for_raw_data()  # 파일 선택 후 텍스트 입력창 호출

    def prompt_for_raw_data(self):
        self.raw_data_window = QWidget()
        self.raw_data_window.setWindowTitle("Input Raw Data")
        self.raw_data_window.setGeometry(100, 100, 800, 600)  # 입력 창의 크기를 조정합니다.

        self.label = QLabel("Enter the raw data:", self.raw_data_window)
        self.label.setGeometry(20, 10, 91, 31)
        self.font = QFont()
        self.font.setPointSize(15)
        self.font.setBold(True)
        self.label.setFont(self.font)

        self.plainTextEdit = QPlainTextEdit(self.raw_data_window)
        self.plainTextEdit.setGeometry(100, 140, 841, 471)
        self.plainTextEdit.setPlaceholderText("Enter the raw data")

        self.submit_button = QPushButton("Submit", self.raw_data_window)
        self.submit_button.setGeometry(200, 620, 100, 31)
        # submit_button.clicked.connect(self.get_text_and_close)

        self.raw_data_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = GRIApp()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())

