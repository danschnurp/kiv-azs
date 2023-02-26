import numpy as np
from matplotlib import pyplot as plt


def show_signal(audio_input, sample_rate=16_000, start=0, ):
    """
    This function takes in an audio signal, sample rate, and start time, and plots the signal in the time domain.

    :param audio_input: the audio signal you want to plot
    :param sample_rate: The sample rate of the audio file
    :param start: the start time of the signal in seconds
    """
    duration = audio_input.shape[0] / float(sample_rate)
    t = np.arange(0, duration, duration / audio_input.shape[0])
    t = np.add(t, start)
    fig, axs = plt.subplots()
    axs.set_title("Signal")
    axs.plot(t, audio_input)
    axs.set_xlabel("Time")
    axs.set_ylabel("Amplitude")
    plt.show()


def show_stats(list_input):
    """
    It shows the stats.

    :param list_input: a list of numbers
    """
    t = np.arange(0, len(list_input))
    fig, axs = plt.subplots()
    axs.set_title("Statistics")
    axs.plot(t, list_input)
    axs.set_xlabel("time")
    axs.set_ylabel("y")
    plt.show()
