# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'audio_cutter.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QMainWindow, QPlainTextEdit, QProgressBar, QPushButton,
    QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(764, 427)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout_graph = QGridLayout()
        self.gridLayout_graph.setObjectName(u"gridLayout_graph")

        self.gridLayout.addLayout(self.gridLayout_graph, 2, 0, 7, 7)

        self.text_input_path = QLineEdit(self.centralwidget)
        self.text_input_path.setObjectName(u"text_input_path")
        self.text_input_path.setReadOnly(False)

        self.gridLayout.addWidget(self.text_input_path, 0, 2, 1, 5)

        self.text_result_paths = QPlainTextEdit(self.centralwidget)
        self.text_result_paths.setObjectName(u"text_result_paths")

        self.gridLayout.addWidget(self.text_result_paths, 0, 8, 9, 1)

        self.pushButton_open_file = QPushButton(self.centralwidget)
        self.pushButton_open_file.setObjectName(u"pushButton_open_file")

        self.gridLayout.addWidget(self.pushButton_open_file, 0, 0, 1, 1)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_5, 0, 1, 1, 1)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.gridLayout_5.addWidget(self.label, 2, 4, 1, 1)

        self.pushButton_mf_analysis = QPushButton(self.centralwidget)
        self.pushButton_mf_analysis.setObjectName(u"pushButton_mf_analysis")

        self.gridLayout_5.addWidget(self.pushButton_mf_analysis, 4, 5, 1, 1)

        self.pushButton_SVM = QPushButton(self.centralwidget)
        self.pushButton_SVM.setObjectName(u"pushButton_SVM")

        self.gridLayout_5.addWidget(self.pushButton_SVM, 2, 5, 1, 1)

        self.line_edit_start_fragment = QLineEdit(self.centralwidget)
        self.line_edit_start_fragment.setObjectName(u"line_edit_start_fragment")

        self.gridLayout_5.addWidget(self.line_edit_start_fragment, 1, 2, 1, 1)

        self.pushButton_VAD = QPushButton(self.centralwidget)
        self.pushButton_VAD.setObjectName(u"pushButton_VAD")

        self.gridLayout_5.addWidget(self.pushButton_VAD, 4, 6, 1, 1)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setTextFormat(Qt.RichText)
        self.label_6.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.label_6, 1, 5, 1, 2)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_5.addWidget(self.label_4, 1, 4, 1, 1)

        self.line_edit_end_fragment = QLineEdit(self.centralwidget)
        self.line_edit_end_fragment.setObjectName(u"line_edit_end_fragment")

        self.gridLayout_5.addWidget(self.line_edit_end_fragment, 2, 2, 1, 1)

        self.pushButton_SIlence = QPushButton(self.centralwidget)
        self.pushButton_SIlence.setObjectName(u"pushButton_SIlence")

        self.gridLayout_5.addWidget(self.pushButton_SIlence, 2, 6, 1, 1)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_3, 2, 0, 1, 2)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_2, 1, 0, 1, 2)

        self.pushButton_play_fragment = QPushButton(self.centralwidget)
        self.pushButton_play_fragment.setObjectName(u"pushButton_play_fragment")

        self.gridLayout_5.addWidget(self.pushButton_play_fragment, 4, 2, 1, 1)

        self.pushButton_stop_fragment = QPushButton(self.centralwidget)
        self.pushButton_stop_fragment.setObjectName(u"pushButton_stop_fragment")

        self.gridLayout_5.addWidget(self.pushButton_stop_fragment, 4, 4, 1, 1)

        self.push_button_view_fragement = QPushButton(self.centralwidget)
        self.push_button_view_fragement.setObjectName(u"push_button_view_fragement")

        self.gridLayout_5.addWidget(self.push_button_view_fragement, 4, 0, 1, 2)


        self.gridLayout.addLayout(self.gridLayout_5, 1, 0, 1, 7)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)
        self.progressBar.setTextVisible(True)

        self.gridLayout.addWidget(self.progressBar, 11, 0, 1, 9)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open...", None))
        self.text_input_path.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Path to input audio file...", None))
        self.text_result_paths.setPlainText(QCoreApplication.translate("MainWindow", u"Here you will see starts of potential time segments...", None))
        self.pushButton_open_file.setText(QCoreApplication.translate("MainWindow", u"Choose Input File", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Input Path:", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"sec", None))
        self.pushButton_mf_analysis.setText(QCoreApplication.translate("MainWindow", u"Male/Female Segments", None))
        self.pushButton_SVM.setText(QCoreApplication.translate("MainWindow", u"SVM", None))
        self.pushButton_VAD.setText(QCoreApplication.translate("MainWindow", u"Voice Activation Detection", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Analysis Starter Buttons", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"sec", None))
        self.pushButton_SIlence.setText(QCoreApplication.translate("MainWindow", u"Silence Segments", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"End of Fragment:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Start of the Fragment:", None))
        self.pushButton_play_fragment.setText(QCoreApplication.translate("MainWindow", u"Play Fragment", None))
        self.pushButton_stop_fragment.setText(QCoreApplication.translate("MainWindow", u"Stop Fragment", None))
        self.push_button_view_fragement.setText(QCoreApplication.translate("MainWindow", u"View Fragment", None))
    # retranslateUi

