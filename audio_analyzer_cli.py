#  date: 15. 01. 2023
#  author: Daniel Schnurpfeil
#
import time

from brain.filters import find_fragments_fft
from utils_and_io.loaders_savers import load_with_ffmpeg, load_fragment_with_ffmpeg


def main(args):
    step = 10
    # The sample rate of the audio file.
    sample_rate = 16000
    t1 = time.time()
    # Converting the argument to a string.
    file_name = str(args.f_input)

    # Loading the fragment signal from the file specified by the `f_fragment` argument.
    fragment_signal = load_fragment_with_ffmpeg(file_name, start=args.start, end=args.end, sample_rate=sample_rate)

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
    find_fragments_fft(signal, fragment_signal, sample_rate)

    # # Using the VAD to find the non-speech parts of the signal.
    # process_with_vad(signal, fragment_signal, sample_rate)

    # translate_fragments(times, remove_duplicates, signal, sample_rate)

    # potential_silence = find_silence(signal, step, 0.1, sample_rate, 0.001)
    # print(len(potential_silence), "potential parts found...")
    # print("translating potential locations of segments...")
    # translate_segments(potential_silence, step)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='audio_cutter')
    parser.add_argument('-i', '--f_input',
                        help='path to input file...', required=True)
    parser.add_argument('-s', '--start', default=1, type=float,
                        help='start of the fragment...')
    parser.add_argument('-e', '--end', default=5, type=float,
                        help='end of the fragment...')

    args = parser.parse_args()
    main(args)
