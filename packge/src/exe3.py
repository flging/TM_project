import sys
import json
import threading
import time
# import filedialog, messagebox, simpledialog
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QWidget, QFileDialog, QMessageBox, QDialog, QInputDialog)
from TM_find_page import find_gri_pages
from TM_agent_getindex import get_index
from TM_extract_text import extract_text_from_pages
from TM_agent import get_draft
from Indextranslate import translate

class GRIApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GRI Draft Generator")
        self.resize(1027, 693)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.label.setGeometry(QRect(-10, 0, 1051, 631))
        self.label.setStyleSheet("background-color:rgb(255, 217, 102)")
        self.label_pic = QLabel(self.centralwidget)
        self.label_pic.setObjectName("label_pic")
        self.label_pic.setGeometry(QRect(400, 220, 241, 91))
        self.label_pic.setStyleSheet("image: url(:/logo1/\ub85c\uace01.png);")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.label_2.setGeometry(QRect(350, 320, 351, 61))
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setGeometry(QRect(200, 400, 671, 91))
        font1 = QFont()
        font1.setPointSize(15)
        self.pushButton.setFont(font1)
        self.pushButton.clicked.connect(self.select_pdf)
        self.pushButton.setStyleSheet("")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 1027, 33))
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.pdf_path = None
        self.raw_data = None
        self.index_list = []
        self.key = None  # key 속성을 추가합니다.
        self.request_key()

    def request_key(self):
    # 사용자로부터 키를 입력받는 메서드입니다.
        key, ok_pressed = QInputDialog.getText(self, "Input", "Please enter the key:")
        if ok_pressed and key:
            self.key = key
        else:
            QMessageBox.warning(self, "Warning", "The key is required to proceed.")
            self.request_key()  # 유효한 키를 받을 때까지 재요청합니다.

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "GRI Draft Generator", None))
        self.label.setText("")
        self.label_pic.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", "초기 보고서를 처리하세요", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", "PDF 파일을 선택하세요", None))

    def select_pdf(self):
        self.pdf_path, _ = QFileDialog.getOpenFileName(self, "Select PDF", "", "PDF files (*.pdf)")
        if self.pdf_path:
            QMessageBox.information(self, "PDF Selected", f"Selected PDF: {self.pdf_path}")
            self.prompt_for_raw_data()

    def prompt_for_raw_data(self):
        self.input_window = QDialog(self)
        self.input_window.setWindowTitle("Input Raw Data")
        self.input_window.setGeometry(100, 100, 1200, 800)

        self.raw_data_text = QTextEdit(self.input_window)
        self.raw_data_text.setGeometry(QRect(50, 50, 1100, 600))
        submit_button = QPushButton("Submit", self.input_window)
        submit_button.setGeometry(QRect(550, 670, 100, 30))
        submit_button.clicked.connect(self.get_text_and_close)
        self.input_window.exec()

    def get_text_and_close(self):
        self.raw_data = self.raw_data_text.toPlainText().strip()  # 텍스트 영역에서 데이터를 가져옵니다.
        if self.raw_data:
            self.load_raw_data()
        else:
            QMessageBox.warning(self, "Warning", "Raw data is required to proceed.")
        self.input_window.close()  # 입력 창을 닫습니다.

    def load_raw_data(self):
        self.get_index_and_titles()

    def get_index_and_titles(self):
        self.index_list = Show_indexList(self.raw_data, self.key)
        titles = get_GRI_Title(self.index_list)
        combined_list = [f"({self.index_list[i]['disclosure_num']}): [{title}] - {self.index_list[i]['description']}" for i, title in enumerate(titles)]
        self.show_items(combined_list)

    def show_items(self, titles):
        self.listbox.delete(0, tk.END)
        for title in titles:
            self.listbox.insert(tk.END, title)
        self.generate_draft_btn.config(state='normal')

    def generate_draft(self):
        selected_indices = [self.listbox.curselection()[i] for i in range(len(self.listbox.curselection()))]
        if len(selected_indices) != 3:
            QMessageBox.error(self, "Error", "Please select exactly 3 items.")
            return
        self.create_draft(selected_indices)

    def create_draft(self, selected_indices):
        draft = []
        for number in selected_indices:
            disclosure_num = self.index_list[number]['disclosure_num']
            pages = find_gri_pages(self.pdf_path, disclosure_num)
            if type(pages) == list:
                extracted_pages = extract_text_from_pages(self.pdf_path, pages)
            else:
                extracted_pages = ["no page in previous report"]
            for extracted_page in extracted_pages:
                small_draft = [pages, disclosure_num]
                small_draft.append(get_draft(extracted_page, disclosure_num, self.raw_data, self.key))
            draft.append(small_draft)
        self.show_draft_result(draft)

    def show_draft_result(self, result):
        # 결과 창 생성
        result_window = QDialog(self)
        result_window.setWindowTitle("Draft Generated")
        result_window.setGeometry(200, 200, 1600, 1000)

        # Result sections for each draft
        for i, draft in enumerate(result):
            # Create a frame for each draft section
            draft_frame = QWidget(result_window)
            draft_frame.setGeometry(QRect(50, 50 + i * 300, 1500, 250))
            draft_frame.setObjectName(f"draft_frame_{i}")

            # Add a label as a header for each section
            header_label = QLabel(f"Draft {i + 1}", draft_frame)
            header_label.setGeometry(QRect(10, 10, 100, 30))
            header_label.setFont(QFont("Arial", 12, QFont.Bold))

            # Add a text widget for each draft content
            draft_text = QTextEdit(draft_frame)
            draft_text.setGeometry(QRect(10, 50, 1480, 180))
            draft_text.setReadOnly(True)
            draft_text.setPlainText("\n".join(str(part) for part in draft))

        close_button = QPushButton("Close", result_window)
        close_button.setGeometry(QRect(700, 900, 100, 30))
        close_button.clicked.connect(result_window.close)

        result_window.exec()

def Show_indexList(raw_data, key):
    index_list = json.loads(get_index(raw_data, key))
    return index_list

def get_GRI_Title(index_list):
    Title_list = []
    for index in index_list:
        gri = index['disclosure_num']
        GRI_title = translate(gri)
        Title_list.append(GRI_title)
    return Title_list


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = GRIApp()
    ui.show()
    sys.exit(app.exec())