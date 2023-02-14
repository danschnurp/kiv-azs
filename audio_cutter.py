#  date: 15. 01. 2023
#  author: Daniel Schnurpfeil
#

import time

import numpy as np
import scipy.signal as sg
from numpy.fft import rfft
from scipy.signal.windows import gaussian
import webrtcvad

from loaders_savers import load_with_ffmpeg
from vad import find_non_speech_parts
from vizualize import show_signal, show_stats


def find_fragments_fft(signal_input: np.ndarray,
                       fragment_signal: np.ndarray,
                       sample_rate: int,
                       window=gaussian(1_000, std=100),
                       max_difference=0.0
                       ) -> tuple:
    """
    > Finds the start and end times of a fragment in a signal using the Fast Fourier Transform

    :param max_difference:
    :param signal_input: the signal you want to search for the fragment in
    :type signal_input: np.ndarray
    :param fragment_signal: the fragment of the signal you want to find
    :type fragment_signal: np.ndarray
    :param sample_rate: the sample rate of the signal_input
    :type sample_rate: int
    :param window: the window function to use
    :param max_difference: the maximum difference between the fragment and the signal
    """
    t1 = time.time()
    iter_step = len(fragment_signal)
    # Convolving the fragmented signal with a window.
    fragment_signal = sg.convolve(fragment_signal, window)
    # Showing the signal in a graph.
    show_signal(fragment_signal, sample_rate)
    exit(0)
    results = []
    stats = []
    # Iterating over the signal in steps of `iter_step` samples.
    for i in range(0, len(signal_input), iter_step):
        # Convolving the signal with a window.
        audio_input = sg.convolve(signal_input[i:int(i + iter_step)], window)
        if len(audio_input) == len(fragment_signal):
            # Taking the FFT of the product of the two signals, and then taking the maximum value of the FFT.
            diff_freq = np.max(np.fft.fft(fragment_signal * audio_input))
            stats.append(diff_freq)
            # Checking if the difference between the two signals is defined difference.
            if diff_freq > max_difference:
                results.append(time.strftime('%H:%M:%S', time.gmtime(i / sample_rate)))
                print(
                    time.strftime('%H:%M:%S', time.gmtime(i / sample_rate))
                )
    print("signal processed in:", time.strftime('%H:%M:%S', time.gmtime(time.time() - t1)))
    return results, stats


def find_fragments_corr(signal_input: np.ndarray, fragment_signal: np.ndarray, sample_rate: int) -> list:
    # IN PROGRESS
    t1 = time.time()
    iter_step = len(fragment_signal)
    results = []
    stats = {}
    for i in range(0, len(signal_input), iter_step):
        audio_input = signal_input[i:int(i + iter_step)]
        if len(audio_input) == len(fragment_signal):
            correlation = sg.correlate(fragment_signal, audio_input, mode="full", method="fft")
            lags = sg.correlation_lags(fragment_signal.size, audio_input.size, mode="full")
            lag = lags[np.argmax(correlation)] / len(lags)
    print("signal processed in:", time.strftime('%H:%M:%S', time.gmtime(time.time() - t1)))
    return results


def process_with_vad(vad, signal=None, fragment_signal=None, sample_rate=None):
    """
    It takes a VAD object, a signal, a fragment of the signal, and a sample rate, and returns a list of the
     fragments of the signal that are considered to be speech.

    :param vad: the vad object
    :param signal: the entire audio signal
    :param fragment_signal: a numpy array of the audio signal
    :param sample_rate: The sample rate of the audio signal
    """
    print("processing signal with VAD...")
    t1 = time.time()
    vad_times, vad_stats, vad_stats2 = find_non_speech_parts(vad, signal, fragment_signal, sample_rate)
    print("signal processed in:", time.strftime('%H:%M:%S', time.gmtime(time.time() - t1)))
    print(vad_times)
    show_stats(vad_stats)
    show_stats(vad_stats2)


def main(args):
    step = 10
    # The sample rate of the audio file.
    sample_rate = 16000
    t1 = time.time()
    # Converting the argument to a string.
    file_name = str(args.f_input)
    start = 0
    end = 2

    # Loading the fragment signal from the file specified by the `f_fragment` argument.
    fragment_signal = load_with_ffmpeg(str(args.f_fragment), sample_rate)

    # sounddevice.play(fragment_signal / sample_rate, sample_rate)
    # show_signal(fragment_signal, sample_rate)
    # print(has_human_voice(fragment_signal, 0.2, sample_rate))

    print("loading file...")
    # Loading the audio file specified by the `file_name` argument, and converting it to a numpy array.
    signal = load_with_ffmpeg(file_name, sample_rate)
    # show_signal(signal, sample_rate)

    print("signal loaded in:", time.strftime('%H:%M:%S', time.gmtime(time.time() - t1)))
    print("signal length is", time.strftime('%H:%M:%S', time.gmtime(int(len(signal) / sample_rate))))

    # Finding the fragments of the signal that are similar to the fragment_signal.
    print("processing signal with my filter...")
    fragment_times, fragment_stats = find_fragments_fft(signal, fragment_signal, sample_rate)
    show_stats(fragment_stats)

    # # Using the VAD to find the non-speech parts of the signal.
    process_with_vad(webrtcvad.Vad(), signal, fragment_signal, sample_rate)

    # translate_fragments(times, remove_duplicates, signal, sample_rate)

    # potential_silence = find_silence(signal, step, 0.1, sample_rate, 0.001)
    # print(len(potential_silence), "potential parts found...")
    # print("translating potential locations of segments...")
    # translate_segments(potential_silence, step)
