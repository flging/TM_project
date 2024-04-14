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
    QPushButton, QSizePolicy, QStatusBar, QWidget, QInputDialog, QMessageBox, QFileDialog, QPlainTextEdit, QFrame, QProgressBar, QListWidgetItem, QScrollArea, QRadioButton)
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
    
    # def get_text_and_close(self):
    #     self.raw_data = self.plainTextEdit.toPlainText().strip()
    #     if self.raw_data:
    #         # 로딩 창 표시
    #         self.show_loading()
    #         # load_raw_data 메서드 호출
    #         self.load_raw_data()

    #         # 여기서 추가 작업 수행
    #     else:
    #         QMessageBox.warning(None, "Warning", "Please enter some text.")
        
    
    # def load_raw_data(self):
    #     self.run_async(self.get_index_and_titles, callback=self.show_items)
    #     self.thread.start()

    # def get_index_and_titles(self):
    #     self.index_list = Show_indexList(self.raw_data, self.key)
    #     titles = get_GRI_Title(self.index_list)
    #     self.combined_list = [f"({self.index_list[i]['disclosure_num']}): [{title}] - {self.index_list[i]['description']}" for i, title in enumerate(titles)]
    #     return self.combined_list
    
    def show_items(self):
        # 이전에 추가된 위젯을 모두 제거합니다.
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
        self.label_2.setFont(font)

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

        self.gri2 = QScrollArea(self.list_window)
        self.gri2.setObjectName(u"gri2")
        self.gri2.setGeometry(QRect(170, 250, 751, 61))
        self.gri2.setStyleSheet(u"border-color: rgb(0, 0, 0); background-color: rgb(255, 255, 255);")
        self.gri2.setWidgetResizable(True)
        self.scrollAreaWidgetContents2 = QWidget()
        self.scrollAreaWidgetContents2.setObjectName(u"gri2_content")
        self.scrollAreaWidgetContents2.setGeometry(QRect(0, 0, 749, 59))
        self.gri2.setWidget(self.scrollAreaWidgetContents2)
        text_label = QLabel(self.combined_list[0], self.scrollAreaWidgetContents2)
        text_label.setGeometry(0, 0, 751, 61)

        self.gri3 = QScrollArea(self.list_window)
        self.gri3.setObjectName(u"gri3")
        self.gri3.setGeometry(QRect(170, 330, 751, 61))
        self.gri3.setStyleSheet(u"border-color: rgb(0, 0, 0); background-color: rgb(255, 255, 255);")
        self.gri3.setWidgetResizable(True)
        self.scrollAreaWidgetContents3 = QWidget()
        self.scrollAreaWidgetContents3.setObjectName(u"gri3_content")
        self.scrollAreaWidgetContents3.setGeometry(QRect(0, 0, 749, 59))
        self.gri3.setWidget(self.scrollAreaWidgetContents3)
        text_label = QLabel(self.combined_list[0], self.scrollAreaWidgetContents3)
        text_label.setGeometry(0, 0, 751, 61)

        self.gri4 = QScrollArea(self.list_window)
        self.gri4.setObjectName(u"gri4")
        self.gri4.setGeometry(QRect(170, 410, 751, 61))
        self.gri4.setStyleSheet(u"border-color: rgb(0, 0, 0); background-color: rgb(255, 255, 255);")
        self.gri4.setWidgetResizable(True)
        self.scrollAreaWidgetContents4 = QWidget()
        self.scrollAreaWidgetContents4.setObjectName(u"gri4_content")
        self.scrollAreaWidgetContents4.setGeometry(QRect(0, 0, 749, 59))
        self.gri4.setWidget(self.scrollAreaWidgetContents4)
        text_label = QLabel(self.combined_list[0], self.scrollAreaWidgetContents4)
        text_label.setGeometry(0, 0, 751, 61)

        self.gri5 = QScrollArea(self.list_window)
        self.gri5.setObjectName(u"gri5")
        self.gri5.setGeometry(QRect(170, 490, 751, 61))
        self.gri5.setStyleSheet(u"border-color: rgb(0, 0, 0); background-color: rgb(255, 255, 255);")
        self.gri5.setWidgetResizable(True)
        self.scrollAreaWidgetContents5 = QWidget()
        self.scrollAreaWidgetContents5.setObjectName(u"gri5_content")
        self.scrollAreaWidgetContents5.setGeometry(QRect(0, 0, 749, 59))
        self.gri5.setWidget(self.scrollAreaWidgetContents5)
        text_label = QLabel(self.combined_list[0], self.scrollAreaWidgetContents5)
        text_label.setGeometry(0, 0, 751, 61)

        self.gricheck1 = QRadioButton(self.list_window)
        self.gricheck1.setObjectName(u"gricheck1")
        self.gricheck1.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.gricheck1.setGeometry(QRect(130, 190, 16, 20))
        
        self.gricheck2 = QRadioButton(self.list_window)
        self.gricheck2.setObjectName(u"gricheck2")
        self.gricheck2.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.gricheck2.setGeometry(QRect(130, 270, 16, 20))
        
        self.gricheck3 = QRadioButton(self.list_window)
        self.gricheck3.setObjectName(u"gricheck3")
        self.gricheck3.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.gricheck3.setGeometry(QRect(130, 350, 16, 20))

        self.gricheck4 = QRadioButton(self.list_window)
        self.gricheck4.setObjectName(u"gricheck4")
        self.gricheck4.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.gricheck4.setGeometry(QRect(130, 430, 16, 20))

        self.gricheck5 = QRadioButton(self.list_window)
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
        # ok_button.clicked.connect(self.edit_text)


        self.list_window.show()


#     def load_raw_data(self):
#         self.run_async(self.get_index_and_titles, callback=self.show_items)
    
#     def get_index_and_titles(self):
#         self.index_list = Show_indexList(self.raw_data, self.key)
#         titles = get_GRI_Title(self.index_list)
#         combined_list = [f"({self.index_list[i]['disclosure_num']}): [{title}] - {self.index_list[i]['description']}" for i, title in enumerate(titles)]
#         return combined_list
    
#     def show_items(self, titles):
#         self.listbox.delete(0, tk.END)
#         for title in titles:
#             self.listbox.insert(tk.END, title)
#         self.generate_draft_btn.config(state='normal')
    
#     def generate_draft(self):
#         selected_indices = [self.listbox.curselection()[i] for i in range(len(self.listbox.curselection()))]
#         if len(selected_indices) != 3:
#          messagebox.showerror("Error", "Please select exactly 3 items.")
#          return
#         self.run_async(self.create_draft, selected_indices, callback=self.show_draft_result)

#     def show_draft_result(self, result):
#     # 결과 창 생성
#         result_window = Toplevel(self)
#         result_window.title("Draft Generated")
#         result_window.geometry("1600x1000")  # Adjust the window size as needed

#         # Result sections for each draft
#         for i, draft in enumerate(result):
#             # Create a frame for each draft section
#             draft_frame = tk.Frame(result_window)
#             draft_frame.pack(fill='both', expand=True)

#             # Add a label as a header for each section
#             header_label = tk.Label(draft_frame, text=f"Draft {i + 1}", font=("Arial", 12, "bold"))
#             header_label.pack(pady=(10, 0))

#             # Add a text widget for each draft content
#             draft_text = tk.Text(draft_frame, height=20, width=100)
#             draft_text.pack(padx=10, pady=5, expand=True, fill='both')
#             draft_text.insert(tk.END, "\n".join(str(part) for part in draft))
#             draft_text.config(state='disabled')  # Make the text widget read-only

#             # If desired, add a separator between sections
#             if i < len(result) - 1:
#                 separator = tk.Frame(result_window, height=2, bd=1, relief="sunken")
#                 separator.pack(fill='x', padx=5, pady=5)

#         # Scrollbar (Optional, add if the text length exceeds the widget size)
#         # You would need to wrap each Text widget or the whole window content in a Scrollable Frame or similar.

#         # 창 닫기 버튼
#         close_button = tk.Button(result_window, text="Close", command=lambda: [result_window.destroy(), self.reset_app()])
#         close_button.pack(pady=10, side='bottom')

#     def reset_app(self):
#     # Reset the application to its initial state
#         self.raw_data = None
#         self.index_list = []
#         self.listbox.delete(0, tk.END)
#         self.load_data_btn.config(state='disabled')
#         self.generate_draft_btn.config(state='disabled')
#         # 결과 창 닫힘 처리를 기다린 후 raw data 입력 창을 열도록 스케줄링
#         self.after(100, self.prompt_for_raw_data)

#     def create_draft(self, selected_indices):
#         return Create_Draft(self.raw_data, self.index_list, selected_indices, self.pdf_path, self.key)
    
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