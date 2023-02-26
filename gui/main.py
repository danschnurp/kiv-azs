#  date: 30. 01. 2023
#  author: Daniel Schnurpfeil
#

import sys

import numpy as np
import sounddevice
from PySide6 import QtWidgets
from PySide6.QtCore import QProcess, QThreadPool
from PySide6.QtWidgets import QFileDialog, QErrorMessage

from gui.fragment_signal_controller import FragmentSignalController
from gui.worker import Worker
from loaders_savers import load_fragment_with_ffmpeg_kwargs
from ui_audio_cutter import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fragment_signal = None
        self.err = QErrorMessage()
        self.player = QProcess()
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)
        self.setupUi(self)
        # It sets the text of the line edit to the string "0".
        self.line_edit_start_fragment.setText(str(0))
        # It sets the text of the line edit to the string "10".
        self.line_edit_end_fragment.setText(str(10))
        self.pushButton_open_file.clicked.connect(self.get_file)
        self.push_button_view_fragement.clicked.connect(self.show_fragment_signal)
        # A variable that is used to store the current signal that is being shown.
        self.showing_signal = None
        self.progressBar.hide()
        self.pushButton_play_fragment.clicked.connect(self.play)
        self.pushButton_stop_fragment.clicked.connect(self.stop)
        self.pushButton_mf_analysis.clicked.connect(self.perform_male_female_analysis)
        self.previous_fragment = {"file_name": "","start": -1,"end": -1}


    def get_file(self):
        """
        It returns the file name of the file that is being read.
        """
        f_name, _ = QFileDialog.getOpenFileName(self, 'Open file',
                                                '../', "Sound files (*.mp3)")
        self.text_input_path.setText(f_name)
        self.load_fragment()

    def load_fragment(self):
        """
        > This function loads a fragment of a signal from a file
        """

        if len(self.text_input_path.text()) == 0:
            self.err.showMessage("Empty path to audio file...")
            return
        if int(self.line_edit_start_fragment.text()) < 0 or \
                int(self.line_edit_start_fragment.text()) > int(self.line_edit_end_fragment.text()):
            self.err.showMessage("Wrong start or end of fragment!!!")
            return

        if self.fragment_signal is not None and self.previous_fragment["file_name"] == self.text_input_path.text() and \
            self.previous_fragment["start"] == int(self.line_edit_start_fragment.text()) and \
            self.previous_fragment["end"] == int(self.line_edit_end_fragment.text()):
            return
        self.previous_fragment = {"file_name": self.text_input_path.text(),
                                                                  "start": int(self.line_edit_start_fragment.text()),
                                                                  "end": int(self.line_edit_end_fragment.text())
                                                                  }

        # Pass the function to execute
        worker = Worker(load_fragment_with_ffmpeg_kwargs, kwargs=self.previous_fragment)  # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.set_fragment_signal)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(worker)

    def progress_fn(self, s):
        if s == 1:
            self.statusbar.showMessage("Fragment text loading!")

    def set_fragment_signal(self, s):
        self.fragment_signal = s

    def thread_complete(self):
        self.statusbar.showMessage("Fragment text loaded...")

    def show_fragment_signal(self):
        """
        It shows the fragment signal
        """
        self.load_fragment()
        if self.fragment_signal is not None:
            signal_view = FragmentSignalController(self.fragment_signal, int(self.line_edit_start_fragment.text()))

            if self.showing_signal is not None:
                self.showing_signal.deleteLater()
                self.gridLayout_graph.replaceWidget(self.showing_signal, signal_view.main)
            else:
                self.gridLayout_graph.addWidget(signal_view.main)
            self.showing_signal = signal_view.main

    def play(self):
        """
        It plays the loaded sound.
        """
        # default sample rate in Hz
        sample_rate = 16_000.
        self.load_fragment()
        if self.fragment_signal is not None:
            self.player.start(sounddevice.play(self.fragment_signal, float(sample_rate)))

    def stop(self):
        self.player.start(sounddevice.play(np.zeros(5), float(16_000.)))

    def perform_male_female_analysis(self):
        self.text_result_paths.appendPlainText("Loading full signal...")

        # signal
        self.text_result_paths.appendPlainText("Performing analysis...")
        # find_fragments_fft(signal_input=signal,
        #                    fragment_signal=self.fragment_signal)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("AUdio segments analyzer")
    window.show()
    window.activateWindow()
    window.raise_()
    app.exec()
