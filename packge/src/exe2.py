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
    QSize, QTime, QUrl, Qt, Signal, QThread)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QWidget, QInputDialog, QMessageBox, QFileDialog, QPlainTextEdit, QFrame, QProgressBar, QListWidgetItem, QScrollArea, QRadioButton, QCheckBox, QLineEdit, QTabWidget)
# import logo1_rc

class WorkerThread(QThread):
    finished = Signal(object)

    def __init__(self, func, args=None, parent=None):
        super().__init__(parent)
        self.func = func
        self.args = args if args is not None else ()

    def run(self):
        result = self.func(*self.args)
        self.finished.emit(result)
    
    # def __del__(self):
    #     self.wait()  # 쓰레드가 종료될 때까지 대기하도록 함

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

        self.pdf_path = None
        self.raw_data = None
        self.index_list = []
        self.key = None  # key 속성을 추가합니다.      
        self.request_key()  #
        self.retranslateUi(MainWindow)


        QMetaObject.connectSlotsByName(MainWindow)

    def show_loading(self):
        self.loading_window = QMainWindow()
        self.loading_window.setWindowTitle("Loading")
        self.loading_window.setGeometry(0, 0, 200, 100)

        self.loading_label = QLabel("Loading, please wait...", self.loading_window)
        self.loading_label.setGeometry(0, 0, 200, 50)

        self.progress_bar = QProgressBar(self.loading_window)
        self.progress_bar.setGeometry(0, 50, 200, 50)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress

        self.start_time = time.time()

        self.loading_window.show()

    def update_loading_label(self):
        if self.loading_window.isVisible():
            elapsed_time = int(time.time() - self.start_time)
            self.loading_label.setText(f"Loading, please wait... {elapsed_time} seconds")

    def hide_loading(self):
        if self.loading_window is not None:
            self.loading_window.close()
    
    # def run_async(self, func, *args, callback=None):
    #     def run():
    #         self.show_loading()
    #         result = func(*args)
    #         self.hide_loading()
    #         if callback:
    #             callback(result)
            
    #     thread = WorkerThread(func=run)
    #     thread.finished.connect(callback)
    #     thread.start()

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

    def select_pdf(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.pdf_path, _ = QFileDialog.getOpenFileName(self.centralwidget, "Select PDF", "", "PDF files (*.pdf)", options=options)
        if self.pdf_path:
            QMessageBox.information(self.centralwidget, "PDF Selected", f"Selected PDF: {self.pdf_path}")
            self.prompt_for_raw_data()  # 파일 선택 후 텍스트 입력창 호출
            
    def prompt_for_raw_data(self):
        MainWindow.close()

        self.input_window = QWidget()
        self.input_window.setWindowTitle("rawdata_input")
        self.input_window.resize(1059, 664)

        # 배경색 설정
        self.input_window.setStyleSheet("background-color: rgb(255, 217, 102);")

        # 라벨 생성
        self.label_2 = QLabel("GS 건설", self.input_window)
        self.label_2.setGeometry(20, 10, 91, 31)
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.label_2.setFont(font)

        # 선 생성
        self.line = QFrame(self.input_window)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(0, 56, 1059, 2))
        self.line.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        # 텍스트 입력 위젯 생성
        self.plainTextEdit = QPlainTextEdit(self.input_window)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setGeometry(QRect(100, 140, 841, 471))
        self.plainTextEdit.setStyleSheet("background-color: white;")
        self.plainTextEdit.setOverwriteMode(True)
        self.plainTextEdit.setCenterOnScroll(True)
        self.plainTextEdit.setPlaceholderText(u"내용을 입력해주세요")
        font1 = QFont()
        font1.setPointSize(9)  # 폰트 크기 설정
        self.plainTextEdit.setFont(font1)  # 설정한 폰트 적용

        # 라벨 생성
        self.label_3 = QLabel("클라이언트 인터뷰, 고객사 성과자료 등 Raw Data를 입력해주세요!", self.input_window)
        self.label_3.setGeometry(QRect(100, 90, 641, 41))
        self.label_3.setFont(font)

        # 확인 버튼 생성
        ok_button = QPushButton("다음", self.input_window)
        ok_button.setGeometry(500, 630, 75, 23)
        ok_button.setStyleSheet(u"background-color: rgb(0, 0, 0); color: rgb(255, 255, 255);")
        ok_button.clicked.connect(self.process_raw_data)


        self.input_window.show()
    
    def process_raw_data(self):
    # 입력된 텍스트 가져오기
        self.raw_data = self.plainTextEdit.toPlainText().strip()
        if self.raw_data:
            # 스레드 시작
            self.show_loading()
            self.thread = WorkerThread(func=self.get_index_and_titles)
            self.thread.finished.connect(self.show_items)
            self.thread.start()
        else:
            QMessageBox.warning(None, "Warning", "Please enter some text.")

    def get_index_and_titles(self):
        # 데이터 처리 작업
        self.index_list = Show_indexList(self.raw_data, self.key)
        titles = get_GRI_Title(self.index_list)
        self.combined_list = [f"({self.index_list[i]['disclosure_num']}): [{title}] - {self.index_list[i]['description']}" for i, title in enumerate(titles)]
        self.disclosure_num_list = [item["disclosure_num"] for item in self.index_list]
    

    
    def show_items(self):
        # 이전에 추가된 위젯을 모두 제거합니다.
        self.input_window.close()
        self.hide_loading()
        # self.input_window.close()
        
        self.list_window = QWidget()
        self.list_window.setWindowTitle("index_select")
        self.list_window.resize(1059, 664)

        # 배경색 설정
        self.list_window.setStyleSheet("background-color: rgb(255, 217, 102);")

        # 라벨 생성
        self.label_4 = QLabel("GS 건설", self.list_window)
        self.label_4.setGeometry(20, 10, 91, 31)
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.label_4.setFont(font)

        self.label_5 = QLabel(self.list_window)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(100, 140, 841, 441))
        self.label_5.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        # 선 생성
        self.line = QFrame(self.list_window)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(0, 56, 1059, 2))
        self.line.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)


        self.gri1 = QScrollArea(self.list_window)
        self.gri1.setObjectName(u"gri1")
        self.gri1.setGeometry(QRect(170, 170, 751, 61))
        self.gri1.setStyleSheet(u"border-color: rgb(0, 0, 0); background-color: rgb(255, 255, 255);")
        self.gri1.setWidgetResizable(True)
        self.scrollAreaWidgetContents1 = QWidget()
        self.scrollAreaWidgetContents1.setObjectName(u"gri1_content")
        self.scrollAreaWidgetContents1.setGeometry(QRect(0, 0, 749, 59))
        self.gri1.setWidget(self.scrollAreaWidgetContents1)
        text_label = QLabel(self.combined_list[0], self.scrollAreaWidgetContents1)
        text_label.setGeometry(0, 0, 751, 61)
        text_label.setWordWrap(True)

        self.gri2 = QScrollArea(self.list_window)
        self.gri2.setObjectName(u"gri2")
        self.gri2.setGeometry(QRect(170, 250, 751, 61))
        self.gri2.setStyleSheet(u"border-color: rgb(0, 0, 0); background-color: rgb(255, 255, 255);")
        self.gri2.setWidgetResizable(True)
        self.scrollAreaWidgetContents2 = QWidget()
        self.scrollAreaWidgetContents2.setObjectName(u"gri2_content")
        self.scrollAreaWidgetContents2.setGeometry(QRect(0, 0, 749, 59))
        self.gri2.setWidget(self.scrollAreaWidgetContents2)
        text_label2 = QLabel(self.combined_list[1], self.scrollAreaWidgetContents2)
        text_label2.setGeometry(0, 0, 751, 61)
        text_label2.setWordWrap(True)

        self.gri3 = QScrollArea(self.list_window)
        self.gri3.setObjectName(u"gri3")
        self.gri3.setGeometry(QRect(170, 330, 751, 61))
        self.gri3.setStyleSheet(u"border-color: rgb(0, 0, 0); background-color: rgb(255, 255, 255);")
        self.gri3.setWidgetResizable(True)
        self.scrollAreaWidgetContents3 = QWidget()
        self.scrollAreaWidgetContents3.setObjectName(u"gri3_content")
        self.scrollAreaWidgetContents3.setGeometry(QRect(0, 0, 749, 59))
        self.gri3.setWidget(self.scrollAreaWidgetContents3)
        text_label3 = QLabel(self.combined_list[2], self.scrollAreaWidgetContents3)
        text_label3.setGeometry(0, 0, 751, 61)
        text_label3.setWordWrap(True)

        self.gri4 = QScrollArea(self.list_window)
        self.gri4.setObjectName(u"gri4")
        self.gri4.setGeometry(QRect(170, 410, 751, 61))
        self.gri4.setStyleSheet(u"border-color: rgb(0, 0, 0); background-color: rgb(255, 255, 255);")
        self.gri4.setWidgetResizable(True)
        self.scrollAreaWidgetContents4 = QWidget()
        self.scrollAreaWidgetContents4.setObjectName(u"gri4_content")
        self.scrollAreaWidgetContents4.setGeometry(QRect(0, 0, 749, 59))
        self.gri4.setWidget(self.scrollAreaWidgetContents4)
        text_label4 = QLabel(self.combined_list[3], self.scrollAreaWidgetContents4)
        text_label4.setGeometry(0, 0, 751, 61)
        text_label4.setWordWrap(True)

        self.gri5 = QScrollArea(self.list_window)
        self.gri5.setObjectName(u"gri5")
        self.gri5.setGeometry(QRect(170, 490, 751, 61))
        self.gri5.setStyleSheet(u"border-color: rgb(0, 0, 0); background-color: rgb(255, 255, 255);")
        self.gri5.setWidgetResizable(True)
        self.scrollAreaWidgetContents5 = QWidget()
        self.scrollAreaWidgetContents5.setObjectName(u"gri5_content")
        self.scrollAreaWidgetContents5.setGeometry(QRect(0, 0, 749, 59))
        self.gri5.setWidget(self.scrollAreaWidgetContents5)
        text_label5 = QLabel(self.combined_list[4], self.scrollAreaWidgetContents5)
        text_label5.setGeometry(0, 0, 751, 61)
        text_label5.setWordWrap(True)

        self.gricheck1 = QCheckBox(self.list_window)
        self.gricheck1.setObjectName(u"gricheck1")
        self.gricheck1.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.gricheck1.setGeometry(QRect(130, 190, 16, 20))
        
        self.gricheck2 = QCheckBox(self.list_window)
        self.gricheck2.setObjectName(u"gricheck2")
        self.gricheck2.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.gricheck2.setGeometry(QRect(130, 270, 16, 20))
        
        self.gricheck3 = QCheckBox(self.list_window)
        self.gricheck3.setObjectName(u"gricheck3")
        self.gricheck3.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.gricheck3.setGeometry(QRect(130, 350, 16, 20))

        self.gricheck4 = QCheckBox(self.list_window)
        self.gricheck4.setObjectName(u"gricheck4")
        self.gricheck4.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.gricheck4.setGeometry(QRect(130, 430, 16, 20))

        self.gricheck5 = QCheckBox(self.list_window)
        self.gricheck5.setObjectName(u"gricheck5")
        self.gricheck5.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.gricheck5.setGeometry(QRect(130, 510, 16, 20))


        # 라벨 생성
        self.label_6 = QLabel("맞춤 GRI Index를 3개 선택해주세요!", self.list_window)
        self.label_6.setGeometry(QRect(100, 90, 641, 41))
        self.label_6.setFont(font)

        # 확인 버튼 생성
        ok_button = QPushButton("다음", self.list_window)
        ok_button.setGeometry(500, 630, 75, 23)
        ok_button.setStyleSheet(u"background-color: rgb(0, 0, 0); color: rgb(255, 255, 255);")
        ok_button.clicked.connect(self.get_checked_items)


        self.list_window.show()
    
    def get_checked_items(self):
        self.checked_items = []
        if self.gricheck1.isChecked():
            self.checked_items.append(0)
        if self.gricheck2.isChecked():
            self.checked_items.append(1)
        if self.gricheck3.isChecked():
            self.checked_items.append(2)
        if self.gricheck4.isChecked():
            self.checked_items.append(3)
        if self.gricheck5.isChecked():
            self.checked_items.append(4)
        
        if len(self.checked_items) == 3:
            self.show_loading()
            self.thread = WorkerThread(func=self.extract_text)
            self.thread.finished.connect(self.edit_text)
            self.thread.start()

        else:
            QMessageBox.critical(self.list_window, "Error", "정확하게 3개 골라주세요.")
        
        

    
    def extract_text(self):
        self.extracted_text=[]
        for number in self.checked_items:
            disclosure_num = self.index_list[number]['disclosure_num']
            pages = find_gri_pages(self.pdf_path, disclosure_num)
            if type(pages) == list:
                self.extracted_text += extract_text_from_pages(self.pdf_path, pages)
            else:
                self.extracted_text += ["no page in previous report"]
        
        # print(self.extracted_text)
        return self.extracted_text



    def edit_text(self):
        self.hide_loading()
        self.list_window.close()
        self.edit_window = QWidget()
        self.edit_window.setWindowTitle("edit_text")
        self.edit_window.resize(1059, 664)

        # 배경색 설정
        self.edit_window.setStyleSheet("background-color: rgb(255, 217, 102);")

        # 라벨 생성
        self.label_7 = QLabel("GS 건설", self.edit_window)
        self.label_7.setGeometry(20, 10, 91, 31)
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.label_7.setFont(font)

        self.label_8 = QLabel(self.edit_window)
        self.label_8.setObjectName(u"label_5")
        self.label_8.setGeometry(QRect(100, 140, 841, 441))
        self.label_8.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        # 선 생성
        self.line = QFrame(self.edit_window)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(0, 56, 1059, 2))
        self.line.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.label_9 = QLabel("GRI Index에 해당하는 전기 보고서 내용을 검수해주세요!", self.edit_window)
        self.label_9.setGeometry(QRect(100, 90, 641, 41))
        self.label_9.setFont(font)
        
        self.tabWidget = QTabWidget(self.edit_window)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(100, 140, 841, 471))
        
        self.tab_1 = QPlainTextEdit(self.extracted_text[0], self.edit_window)
        self.tab_1.setObjectName(u"tab_1")
        self.tab_1.setGeometry(QRect(100, 140, 841, 471))
        self.tab_1.setStyleSheet("background-color: white;")
        font1 = QFont()
        font1.setPointSize(9)  # 폰트 크기 설정
        self.tab_1.setFont(font1)
        self.tabWidget.addTab(self.tab_1, self.disclosure_num_list[0])

        self.tab_2 = QPlainTextEdit(self.extracted_text[1], self.edit_window)
        self.tab_2.setObjectName(u"tab_2")
        self.tab_2.setGeometry(QRect(100, 140, 841, 471))
        self.tab_2.setStyleSheet("background-color: white;")
        self.tab_2.setFont(font1)
        self.tabWidget.addTab(self.tab_2, self.disclosure_num_list[1])

        self.tab_3 = QPlainTextEdit(self.extracted_text[2], self.edit_window)
        self.tab_3.setObjectName(u"tab_3")
        self.tab_3.setGeometry(QRect(100, 140, 841, 471))
        self.tab_3.setStyleSheet("background-color: white;")
        self.tab_3.setFont(font1)
        self.tabWidget.addTab(self.tab_3, self.disclosure_num_list[2])

        self.tab_4 = QPlainTextEdit(self.extracted_text[3], self.edit_window)
        self.tab_4.setObjectName(u"tab_4")
        self.tab_4.setGeometry(QRect(100, 140, 841, 471))
        self.tab_4.setStyleSheet("background-color: white;")
        self.tab_4.setFont(font1)
        self.tabWidget.addTab(self.tab_4, self.disclosure_num_list[3])

        self.tab_5 = QPlainTextEdit(self.extracted_text[4], self.edit_window)
        self.tab_5.setObjectName(u"tab_5")
        self.tab_5.setGeometry(QRect(100, 140, 841, 471))
        self.tab_5.setStyleSheet("background-color: white;")
        self.tab_5.setFont(font1)
        self.tabWidget.addTab(self.tab_5, self.disclosure_num_list[4])

        submit_button = QPushButton("초안 요청", self.edit_window)
        submit_button.setGeometry(500, 630, 75, 23)
        submit_button.setStyleSheet(u"background-color: rgb(0, 0, 0); color: rgb(255, 255, 255);")
        submit_button.clicked.connect(self.process_edit_text)

        self.edit_window.show()
    
    def process_edit_text(self):
    # 입력된 텍스트 가져오기
        self.text_data1 = self.tab_1.toPlainText().strip()
        self.text_data2 = self.tab_2.toPlainText().strip()
        self.text_data3 = self.tab_3.toPlainText().strip()
        self.text_data4 = self.tab_4.toPlainText().strip()
        self.text_data5 = self.tab_5.toPlainText().strip()

        if self.text_data1 and self.text_data2 and self.text_data3 and self.text_data4 and self.text_data5:
            # 스레드 시작
            self.show_loading()
            self.thread = WorkerThread(func=self.generate_draft)
            self.thread.finished.connect(self.show_draft)
            self.thread.start()
        else:
            QMessageBox.warning(None, "Warning", "Please enter some text.")
    
    def generate_draft(self):
        self.draft1 = get_draft(self.text_data1, self.disclosure_num_list[0], self.raw_data, self.key)
        self.draft2 = get_draft(self.text_data2, self.disclosure_num_list[1], self.raw_data, self.key)
        self.draft3 = get_draft(self.text_data3, self.disclosure_num_list[2], self.raw_data, self.key)
        self.draft4 = get_draft(self.text_data4, self.disclosure_num_list[3], self.raw_data, self.key)
        self.draft5 = get_draft(self.text_data5, self.disclosure_num_list[4], self.raw_data, self.key)


    def show_draft(self):
        self.hide_loading()
        self.edit_window.close()
        self.result_window = QWidget()
        self.result_window.setWindowTitle("edit_text")
        self.result_window.resize(1059, 664)

        # 배경색 설정
        self.result_window.setStyleSheet("background-color: rgb(255, 217, 102);")

        # 라벨 생성
        self.label_10 = QLabel("GS 건설", self.result_window)
        self.label_10.setGeometry(20, 10, 91, 31)
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.label_10.setFont(font)

        self.label_11 = QLabel(self.result_window)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(100, 140, 841, 441))
        self.label_11.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        # 선 생성
        self.line = QFrame(self.result_window)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(0, 56, 1059, 2))
        self.line.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.label_12 = QLabel("ESG 보고서 초안", self.edit_window)
        self.label_12.setGeometry(QRect(100, 90, 641, 41))
        self.label_12.setFont(font)
        
        self.tabWidget2 = QTabWidget(self.result_window)
        self.tabWidget2.setObjectName(u"tabWidget")
        self.tabWidget2.setGeometry(QRect(100, 140, 841, 471))
        
        self.tab_6 = QLabel(str(self.draft1), self.result_window)
        self.tab_6.setObjectName(u"tab_6")
        self.tab_6.setGeometry(QRect(100, 140, 841, 471))
        self.tab_6.setStyleSheet("background-color: white;")
        font1 = QFont()
        font1.setPointSize(9)  # 폰트 크기 설정
        self.tab_6.setFont(font1)
        self.tabWidget2.addTab(self.tab_6, self.disclosure_num_list[0])

        self.tab_7 = QLabel(str(self.draft2), self.result_window)
        self.tab_7.setObjectName(u"tab_7")
        self.tab_7.setGeometry(QRect(100, 140, 841, 471))
        self.tab_7.setStyleSheet("background-color: white;")
        self.tab_7.setFont(font1)
        self.tabWidget2.addTab(self.tab_7, self.disclosure_num_list[1])

        self.tab_8 = QLabel(str(self.draft3), self.result_window)
        self.tab_8.setObjectName(u"tab_8")
        self.tab_8.setGeometry(QRect(100, 140, 841, 471))
        self.tab_8.setStyleSheet("background-color: white;")
        self.tab_8.setFont(font1)
        self.tabWidget2.addTab(self.tab_8, self.disclosure_num_list[2])

        self.tab_9 = QLabel(str(self.draft4), self.result_window)
        self.tab_9.setObjectName(u"tab_9")
        self.tab_9.setGeometry(QRect(100, 140, 841, 471))
        self.tab_9.setStyleSheet("background-color: white;")
        self.tab_9.setFont(font1)
        self.tabWidget2.addTab(self.tab_9, self.disclosure_num_list[3])

        self.tab_10 = QLabel(str(self.draft5), self.result_window)
        self.tab_10.setObjectName(u"tab_10")
        self.tab_10.setGeometry(QRect(100, 140, 841, 471))
        self.tab_10.setStyleSheet("background-color: white;")
        self.tab_10.setFont(font1)
        self.tabWidget2.addTab(self.tab_10, self.disclosure_num_list[4])

        submit_button = QPushButton("다시하기", self.result_window)
        submit_button.setGeometry(500, 630, 75, 23)
        submit_button.setStyleSheet(u"background-color: rgb(0, 0, 0); color: rgb(255, 255, 255);")
        # submit_button.clicked.connect(self.process_edit_text)

        self.result_window.show()

def Show_indexList(raw_data, key):
    index_list = get_index(raw_data, key)
    return index_list

def Create_Draft(raw_data, index_list, selected_numbers, pdf_path, key):
    draft = []
    for number in selected_numbers:
        disclosure_num = index_list[number]['disclosure_num']
        pages = find_gri_pages(pdf_path, disclosure_num)
        if type(pages) == list:
            extracted_pages = extract_text_from_pages(pdf_path, pages)
        else:
            extracted_pages = ["no page in previous report"]
        for extracted_page in extracted_pages:
            small_draft = [pages, disclosure_num]
            small_draft.append(get_draft(extracted_page, disclosure_num, raw_data,key))
        draft.append(small_draft)
    return draft

def get_GRI_Title(index_list):
    Title_list = []
    for index in index_list:
        gri = index['disclosure_num']
        GRI_title = translate(gri)
        Title_list.append(GRI_title)
    return Title_list


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = GRIApp()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())