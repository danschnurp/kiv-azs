import time


def find_silence(signal, step, overlay, sample_rate, ratio):
    """
    It takes a signal, splits it into chunks of length `step` with an overlap of `overlay`, and returns the indices of the
    chunks that are below a certain threshold

    :param signal: the audio signal
    :param step: the number of seconds to step forward in the audio file
    :param overlay: the number of samples to overlap between each step
    :param sample_rate: the sample rate of the audio file
    :param ratio: the ratio of silence to noise
    """
    potential_silence = []
    iter_step = step * sample_rate
    for i in range(0, len(signal), iter_step):
        audio_input = signal[i:int(i + iter_step * (overlay + 1))]
        # show_signal(audio_input, sample_rate, start=0)
        audio_input = audio_input[audio_input < ratio]
        audio_input = audio_input[audio_input > -ratio]

        if len(audio_input) > 5_000:
            potential_silence.append(i / sample_rate)
            print(
                # "silence in:",
                time.strftime('%H:%M:%S', time.gmtime(i / sample_rate))
                # , "+ 10 sec", "in sec:", i
            )
    return potential_silence