#  date: 30. 01. 2023
#  author: Daniel Schnurpfeil
#
import time

import numpy as np
import sounddevice
from PySide6 import QtWidgets
from PySide6.QtCore import QProcess, QThreadPool
from PySide6.QtWidgets import QFileDialog, QErrorMessage, QMessageBox

from brain.filters import find_fragments_fft_kwargs, process_with_vad_kwargs
from gui.fragment_signal_controller import FragmentSignalController
from gui.ui_audio_cutter import Ui_MainWindow
from gui.worker import Worker
from utils_and_io.loaders_savers import load_fragment_with_ffmpeg_kwargs, load_full_with_ffmpeg_kwargs


# The MainWindow class inherits from the QtWidgets.QMainWindow class and the Ui_MainWindow class.
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # A variable that is used to store the fragment signal.
        self.fragment_signal = None
        self.previous_full_signal = None
        self.full_signal = None
        self.full_signal_loader_runs = False
        self.analysis_runs = False
        self.analysis_worker = None
        self.err = QErrorMessage()
        self.player = QProcess()
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)
        self.setupUi(self)
        # It sets the text of the line edit to the string "0".
        self.line_edit_start_fragment.setText(str(0))
        # It sets the text of the line edit to the string "10".
        self.line_edit_end_fragment.setText(str(10))
        self.pushButton_open_file.pressed.connect(self.get_file)
        self.push_button_view_fragement.pressed.connect(self.show_fragment_signal)
        # A variable that is used to store the current signal that is being shown.
        self.showing_signal = None
        self.progressBar.hide()
        self.pushButton_play_fragment.pressed.connect(self.play)
        self.pushButton_stop_fragment.pressed.connect(self.stop)
        self.pushButton_mf_analysis.pressed.connect(self.perform_male_female_analysis)
        self.pushButton_VAD.pressed.connect(self.perform_VAD_analysis)
        # Used to store the previous fragment that was loaded.
        self.previous_fragment = {"file_name": "", "start": -1, "end": -1}

    def get_file(self):
        """
        It returns the file name of the file that is being read.
        """
        f_name, _ = QFileDialog.getOpenFileName(self, 'Open file',
                                                '../', "Sound files (*)")
        # It sets the text of the line edit
        self.text_input_path.setText(f_name)
        self.load_fragment()

    def load_fragment(self):
        """
        > This function loads a fragment of a signal from a file
        """

        # Checking if the analysis is running. If it is running, it shows a dialog box. If the user clicks
        # yes, it stops the analysis. If the user clicks no, it returns.
        if self.analysis_runs:
            dialog = QMessageBox.question(self, "Warning","You are about to stop RUNNING analyis!")
            if dialog == QMessageBox.Yes:
                self.stop_analysis()
            else:
                return

        # It checks if the text input path is empty. If it is empty, it shows an error message.
        if len(self.text_input_path.text()) == 0:
            self.err.showMessage("Empty path to audio file...")
            return
        # It checks if the start of the fragment is less than 0 or if the start of
        # the fragment is greater than the end of the fragment. If it is, it shows an error message.
        if float(self.line_edit_start_fragment.text()) < 0 or \
                float(self.line_edit_start_fragment.text()) > float(self.line_edit_end_fragment.text()):
            self.err.showMessage("Wrong start or end of fragment!!!")
            return

        # It checks if the fragment signal is not None and if the previous fragment is the same as the current fragment.
        if self.fragment_signal is not None and self.previous_fragment["file_name"] == self.text_input_path.text() and \
                self.previous_fragment["start"] == float(self.line_edit_start_fragment.text()) and \
                self.previous_fragment["end"] == float(self.line_edit_end_fragment.text()):
            return
        # Used to store the previous fragment that was loaded.
        self.previous_fragment = {"file_name": self.text_input_path.text(),
                                  "start": float(self.line_edit_start_fragment.text()),
                                  "end": float(self.line_edit_end_fragment.text())
                                  }

        # Pass the function to execute
        worker = Worker(load_fragment_with_ffmpeg_kwargs, kwargs=self.previous_fragment)
        # Connecting the signals to the functions.
        worker.signals.result.connect(self.set_fragment_signal)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        # Execute
        self.threadpool.start(worker)

    def show_fragment_signal(self):
        """
        It shows the fragment signal
        """
        self.load_fragment()
        self.load_full_signal()
        if self.fragment_signal is not None:
            signal_view = FragmentSignalController(self.fragment_signal, float(self.line_edit_start_fragment.text()))

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
        # Used to stop the sound.
        self.player.start(sounddevice.play(np.zeros(5), float(16_000.)))

    def load_full_signal(self):

        if self.full_signal_loader_runs:
            return

        # It checks if the fragment signal is not None and if the previous fragment is the same as the current fragment.
        if self.full_signal is not None and self.previous_full_signal["file_name"] == self.text_input_path.text():
            return
        # Used to store the previous fragment that was loaded.
        self.previous_full_signal = {"file_name": self.text_input_path.text()
                                     }
        # Pass the function to execute
        worker = Worker(load_full_with_ffmpeg_kwargs, kwargs=self.previous_full_signal)
        # Connecting the signals to the functions.
        worker.signals.result.connect(self.set_full_signal)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn_full)

        # Execute
        self.threadpool.start(worker)

    def perform_male_female_analysis(self):
        """
        performs male/female voice analysis with fft
        """
        self.perform_analysis()

    def perform_VAD_analysis(self):
        """
        performs voice activation detection
        """
        self.perform_analysis(worker_method=process_with_vad_kwargs)

    def perform_analysis(self, worker_method=find_fragments_fft_kwargs):
        """
        performs custom analysis
        """

        if self.analysis_runs:
            return

        self.load_full_signal()
        if self.full_signal is None:
            self.err.showMessage("Input audio signal is not loaded yet.")
            return

        self.analysis_worker = Worker(find_fragments_fft_kwargs, kwargs={"signal_input": self.full_signal,
                                                           "fragment_signal": self.fragment_signal})
        self.analysis_worker.signals.result.connect(self.show_stats)
        self.analysis_worker.signals.finished.connect(self.analysis_done)
        self.analysis_worker.signals.progress.connect(self.progress_fn_analysis)

        # Execute
        self.threadpool.start(self.analysis_worker)

    def progress_fn(self, signal_code):
        """
        It prints the progress of the current operation
        :param signal_code: The current state of the process
        """
        if signal_code == 1:
            self.statusbar.showMessage("Fragment signal loading!")

    def progress_fn_full(self, signal_code):
        """
        It prints the progress of the current operation
        :param signal_code: The current state of the process
        """
        if signal_code == 1:
            self.full_signal_loader_runs = True
            self.text_result_paths.clear()
            self.text_result_paths.appendPlainText("Full signal loading!")

    def set_fragment_signal(self, result):
        """
        setter
        :param result: The result of the fragment
        """
        self.fragment_signal = result

    def set_full_signal(self, result):
        """
        setter
        :param result: The result async task
        """
        self.full_signal = result[0]
        self.text_result_paths.appendPlainText(result[1])
        self.text_result_paths.appendPlainText(
            str("signal length is " + time.strftime('%H:%M:%S', time.gmtime(int(len(result[0]) / result[2])))))

    def analysis_done(self):
        """
        This function is called when the analysis is done
        """
        self.text_result_paths.appendPlainText("Analysis done!")
        self.analysis_runs = False

    def stop_analysis(self):
        """
        It stops the analysis.
        """
        self.full_signal_loader_runs = False
        self.analysis_worker.quit()
        self.text_result_paths.appendPlainText("Analysis stopped.")


    def thread_complete(self):
        """
        The function is called when the thread is complete
        """
        self.statusbar.showMessage("Signal loaded...")
        self.full_signal_loader_runs = False

    def progress_fn_analysis(self, signal_code):
        """
        The function is called by the analysis thread and it updates the GUI with the progress of the analysis
        """
        if signal_code == 1:
            self.analysis_runs = True
            self.text_result_paths.clear()
            self.text_result_paths.appendPlainText("Performing analysis...\n")
        else:
            self.text_result_paths.appendPlainText(time.strftime('%H:%M:%S', time.gmtime(signal_code)) + "\n")

    def show_stats(self, stats):
        self.text_result_paths.appendPlainText(stats)
