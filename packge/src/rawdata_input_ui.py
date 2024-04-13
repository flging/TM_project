from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QPlainTextEdit,
    QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1059, 664)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(-10, 0, 1051, 651))
        self.label.setStyleSheet(u"background-color:rgb(255, 217, 102)")
        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(0, 56, 1041, 2))
        self.line.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 10, 91, 31))
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.label_2.setFont(font)
        self.plainTextEdit = QPlainTextEdit(Form)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setGeometry(QRect(100, 140, 841, 471))
        self.plainTextEdit.setOverwriteMode(True)
        self.plainTextEdit.setCenterOnScroll(True)
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(100, 90, 641, 41))
        self.label_3.setFont(font)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText("")
        self.label_2.setText(QCoreApplication.translate("Form", u"GS\uac74\uc124", None))
        self.plainTextEdit.setPlaceholderText(QCoreApplication.translate("Form", u"\ub0b4\uc6a9\uc744 \uc785\ub825\ud574\uc8fc\uc138\uc694", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\ud074\ub77c\uc774\uc5b8\ud2b8 \uc778\ud130\ubdf0, \uace0\uac1d\uc0ac \uc131\uacfc\uc790\ub8cc \ub4f1 Raw Data\ub97c \uc785\ub825\ud574\uc8fc\uc138\uc694!", None))
    # retranslateUi