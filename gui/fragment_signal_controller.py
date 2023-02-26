#  date: 30. 01. 2023
#  author: Daniel Schnurpfeil
#


import numpy as np
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


# This class is a controller for a fragment signal
class FragmentSignalController(QtWidgets.QWidget):

    def __init__(self, input_data, offset):
        super().__init__()
        self._main = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(self._main)

        self.input_data = input_data
        self.time_series = self.get_signal_times(start=offset)

        static_canvas = FigureCanvas(Figure(figsize=(6, 5)))
        layout.addWidget(static_canvas)
        layout.addWidget(NavigationToolbar(static_canvas, self))


        self._static_ax = static_canvas.figure.subplots()

        self._static_ax.plot(self.time_series, self.input_data)

    def get_signal_times(self, sample_rate=16_000, start=0, ):
        """
        This function takes in an audio signal, sample rate, and start time, and plots the signal in the time domain.

        :param audio_input: the audio signal you want to plot
        :param sample_rate: The sample rate of the audio file
        :param start: the start time of the signal in seconds
        """
        duration = self.input_data.shape[0] / float(sample_rate)
        t = np.arange(0, duration, duration / self.input_data.shape[0])
        t = np.add(t, start)
        return t

    @property
    def main(self):
        return self._main
