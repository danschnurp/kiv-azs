import time

import numpy as np

from utils_and_io.utils import add_to_stats_dictionary, show_few_bests


class Frame(object):
    """Represents a "frame" of audio data."""
    def __init__(self, bytes, timestamp, duration):
        self.bytes = bytes
        self.timestamp = timestamp
        self.duration = duration


def frame_generator(frame_duration_ms, audio, sample_rate):
    """Generates audio frames from PCM audio data.
    Takes the desired frame duration in milliseconds, the PCM data, and
    the sample rate.
    Yields Frames of the requested duration.
    """
    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
    offset = 0
    timestamp = 0.0
    duration = (float(n) / sample_rate) / 2.0
    while offset + n < len(audio):
        yield Frame(audio[offset:offset + n], timestamp, duration)
        timestamp += duration
        offset += n


def vad_classifier(sample_rate, vad, frames):
    """
    It takes in a sample rate, a VAD object, and a list of frames, and returns a list of the same length as the input list,
    where each element is either 1 or 0, depending on whether the corresponding frame is speech or not.

    :param sample_rate: The sample rate of the audio file
    :param vad: a webrtcvad.Vad() object
    :param frames: a list of audio frames
    """
    voiced_frames = 0
    for frame in frames:
        is_speech = vad.is_speech(frame.bytes, sample_rate)
        if not is_speech:
            voiced_frames += 1

    return abs(voiced_frames / len(frames))


def no_human_voice(audio, sample_rate, vad):
    """
    > This function takes in an audio file and its sample rate, and returns a list of the audio file's time stamps where
    there is no human voice

    :param audio: the audio file to be processed
    :param sample_rate: The sample rate of the audio file
    """
    frames = frame_generator(30, audio, sample_rate)
    frames = list(frames)
    return vad_classifier(sample_rate, vad, frames)


def find_non_speech_parts(vad, signal_input: np.ndarray, fragment_signal: np.ndarray, sample_rate=0) -> tuple:
    """
    > This function takes in a signal and a fragment of that signal, and returns a list of the non-speech parts of the
    signal

    :param signal_input: the original signal
    :type signal_input: np.ndarray
    :param fragment_signal: the signal that you want to find in the signal_input
    :type fragment_signal: np.ndarray
    :param sample_rate: the sample rate of the signal_input, defaults to 0 (optional)
    """
    iter_step = int(1 * sample_rate)
    print("len(fragment_signal)", len(fragment_signal))
    results = []
    stats = []
    stats2 = []
    stat_dict = {}
    # Iterating over the signal in steps of `iter_step` samples.
    for i in range(0, len(signal_input), iter_step):
        # Convolving the signal with a gaussian window.
        audio_input = signal_input[i:int(i + iter_step)]
        if len(audio_input) == len(fragment_signal):
            stats.append(no_human_voice(audio_input, sample_rate, vad))
            stat_dict = add_to_stats_dictionary(stat_dict, stats[-1], int(i / sample_rate))
            if stats[-1] > 0.95:
                stats2.append(stats[-1])
                results.append(time.strftime('%H:%M:%S', time.gmtime(i / sample_rate)))
    show_few_bests(stat_dict, 10)
    return results, stats, stats2
