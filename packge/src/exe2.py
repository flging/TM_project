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
    QPushButton, QSizePolicy, QStatusBar, QWidget)
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
        self.label_pic.setStyleSheet(u"image: url(:/logo1/\ub85c\uace01.png);")
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
        self.key = simpledialog.askstring("Input", "Please enter the key:",
                                          parent=self)
        if not self.key:
            messagebox.showwarning("Warning", "The key is required to proceed.")
            self.request_key()  # 유효한 키를 받을 때까지 재요청합니다

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"GRI Draft Generator", None))
        self.label.setText("")
        self.label_pic.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\uc804\uae30 \ubcf4\uace0\uc11c\ub97c \ucca8\ubd80\ud574\uc8fc\uc138\uc694", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PDF \ud30c\uc77c\uc744 \ucca8\ubd80\ud574\uc8fc\uc138\uc694", None))
    # retranslateUi

    def select_pdf(self):
            self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
            if self.pdf_path:
                messagebox.showinfo("PDF Selected", f"Selected PDF: {self.pdf_path}")
                self.prompt_for_raw_data()  # 파일 선택 후 텍스트 입력창 호출

    def prompt_for_raw_data(self):
            self.input_window = Toplevel(self)
            self.input_window.title("Input Raw Data")
            self.input_window.geometry("1200x800")  # 입력 창의 크기를 조정합니다.

            tk.Label(self.input_window, text="Enter the raw data:").pack(pady=10)

            self.raw_data_text = tk.Text(self.input_window, height=40, width=150)
            self.raw_data_text.pack(pady=10)

            submit_button = tk.Button(self.input_window, text="Submit", command=self.get_text_and_close)
            submit_button.pack(pady=10)

    def get_text_and_close(self):
        self.raw_data = self.raw_data_text.get("1.0", tk.END).strip()  # 텍스트 영역에서 데이터를 가져옵니다.
        if self.raw_data:
            self.load_data_btn.config(state='normal')
        else:
            self.load_data_btn.config(state='disabled')
        self.input_window.destroy()  # 입력 창을 닫습니다.

    def load_raw_data(self):
        self.run_async(self.get_index_and_titles, callback=self.show_items)
    
    def get_index_and_titles(self):
        self.index_list = Show_indexList(self.raw_data, self.key)
        titles = get_GRI_Title(self.index_list)
        combined_list = [f"({self.index_list[i]['disclosure_num']}): [{title}] - {self.index_list[i]['description']}" for i, title in enumerate(titles)]
        return combined_list
    
    def show_items(self, titles):
        self.listbox.delete(0, tk.END)
        for title in titles:
            self.listbox.insert(tk.END, title)
        self.generate_draft_btn.config(state='normal')
    
    def generate_draft(self):
        selected_indices = [self.listbox.curselection()[i] for i in range(len(self.listbox.curselection()))]
        if len(selected_indices) != 3:
         messagebox.showerror("Error", "Please select exactly 3 items.")
         return
        self.run_async(self.create_draft, selected_indices, callback=self.show_draft_result)

    def show_draft_result(self, result):
    # 결과 창 생성
        result_window = Toplevel(self)
        result_window.title("Draft Generated")
        result_window.geometry("1600x1000")  # Adjust the window size as needed

        # Result sections for each draft
        for i, draft in enumerate(result):
            # Create a frame for each draft section
            draft_frame = tk.Frame(result_window)
            draft_frame.pack(fill='both', expand=True)

            # Add a label as a header for each section
            header_label = tk.Label(draft_frame, text=f"Draft {i + 1}", font=("Arial", 12, "bold"))
            header_label.pack(pady=(10, 0))

            # Add a text widget for each draft content
            draft_text = tk.Text(draft_frame, height=20, width=100)
            draft_text.pack(padx=10, pady=5, expand=True, fill='both')
            draft_text.insert(tk.END, "\n".join(str(part) for part in draft))
            draft_text.config(state='disabled')  # Make the text widget read-only

            # If desired, add a separator between sections
            if i < len(result) - 1:
                separator = tk.Frame(result_window, height=2, bd=1, relief="sunken")
                separator.pack(fill='x', padx=5, pady=5)

        # Scrollbar (Optional, add if the text length exceeds the widget size)
        # You would need to wrap each Text widget or the whole window content in a Scrollable Frame or similar.

        # 창 닫기 버튼
        close_button = tk.Button(result_window, text="Close", command=lambda: [result_window.destroy(), self.reset_app()])
        close_button.pack(pady=10, side='bottom')

    def reset_app(self):
    # Reset the application to its initial state
        self.raw_data = None
        self.index_list = []
        self.listbox.delete(0, tk.END)
        self.load_data_btn.config(state='disabled')
        self.generate_draft_btn.config(state='disabled')
        # 결과 창 닫힘 처리를 기다린 후 raw data 입력 창을 열도록 스케줄링
        self.after(100, self.prompt_for_raw_data)

    def create_draft(self, selected_indices):
        return Create_Draft(self.raw_data, self.index_list, selected_indices, self.pdf_path, self.key)
    
def Show_indexList(raw_data, key):
    index_list = json.loads(get_index(raw_data, key))
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