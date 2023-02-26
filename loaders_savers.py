import ffmpeg
import numpy as np


def load_with_ffmpeg(file_name, sample_rate=16_000):
    """
    It loads a file using ffmpeg, and returns the data as a numpy array

    :param file_name: The path to the audio file
    :param sample_rate: The number of samples per second of audio
    """
    audio_ch0 = ffmpeg.input(file_name)['a:0'] \
        .filter('channelsplit', channel_layout='mono', channels='FC') \
        .output('pipe:', loglevel=0, format='s16le', acodec='pcm_s16le', ac=1, ar=str(sample_rate)) \
        .run(capture_stdout=True)

    return np.frombuffer(audio_ch0[0], np.int16)


def save_fragment_with_ffmpeg(file_name, start, end):
    """
    It takes a file name, a start time, and an end time, and saves a fragment of the video file between those times

    :param file_name: The name of the file to be processed
    :param start: the start time of the fragment in seconds
    :param end: the end time of the fragment
    """
    name = file_name.replace("\\", "/")
    name = name.split("/")
    ffmpeg.input(file_name, ss=start,
                 t=end - start).output(
        "./" + "fragment_" + name[-1]).run(capture_stdout=True, overwrite_output=True)


def load_fragment_with_ffmpeg_kwargs(kwargs):
    """
    It takes a dictionary of keyword arguments, and returns a fragment of an audio
    :param kwargs: a dictionary of keyword arguments to pass to ffmpeg
    """
    file_name = kwargs["file_name"]
    start = kwargs["start"]
    end = kwargs["end"]
    # Emitting a signal to the gui with code "1".
    kwargs["progress_callback"].emit(1)
    return load_fragment_with_ffmpeg(file_name, start, end)


def load_fragment_with_ffmpeg(file_name, start, end, sample_rate=16_000):
    """
    It loads a fragment of a sound file, resamples it to a given sample rate, and returns the fragment as a numpy array

    :param file_name: the name of the file to load
    :param start: start time of the fragment in seconds
    :param end: end time of the fragment in seconds
    :param sample_rate: the sample rate of the audio file
    """
    audio_ch0 = ffmpeg.input(file_name, ss=start,
                             t=end - start)['a:0'] \
        .filter('channelsplit', channel_layout='mono', channels='FC') \
        .output('pipe:', loglevel=0, format='s16le', acodec='pcm_s16le', ac=1, ar=str(sample_rate)) \
        .run(capture_stdout=True)
    return np.frombuffer(audio_ch0[0], np.int16)


def load_waw(input, start=0, stop=None):
    """
    loads waw
    :param input: path to file
    :param start: beginning of sample
    :param stop: end of sample based on input
    :return: tuple(audio_sample, sample_rate)
    """
    import soundfile as sf
    return sf.read(input, start=start, stop=stop)


def load_mp3(input, offset=0, duration=None):
    """
    loads mp3 signal
    :param input: path to file
    :param offset: beginning of sample
    :param duration: duration from offset
    :return: tuple(audio_sample, sample_rate)
    """
    import librosa
    return librosa.load(input, offset=offset, duration=duration)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='save_fragment_with_ffmpeg')
    parser.add_argument('-i', '--f_input',
                        help='path to input file...', required=True)
    parser.add_argument('-s', '--start', required=True)
    parser.add_argument('-e', '--end', required=True)
    args = parser.parse_args()
    save_fragment_with_ffmpeg(args.f_input, int(args.start), int(args.end))
