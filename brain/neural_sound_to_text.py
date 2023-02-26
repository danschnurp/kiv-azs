import time

import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor


def translate_segments(potential_silence, step, signal, sample_rate):
    """
    It takes a signal, and prints a list of tuples, each tuple containing the start and end times of a segment of the
    signal

    :param potential_silence: a list of tuples, each tuple is a segment of silence
    :param step: the number of samples to move the window forward
    :param signal: the audio signal we're working with
    :param sample_rate: the sample rate of the audio file
    """
    p, m = init_neural_nett()
    t1 = time.time()
    overlay = 10
    for i in potential_silence:
        if i > 0:
            described_speech = cz_speech_to_text(
                signal[int(i - overlay) * sample_rate:int(i + step + overlay) * sample_rate],
                sample_rate, p, m)
        else:
            described_speech = cz_speech_to_text(signal[int(i) * sample_rate:int(i + step) * sample_rate],
                                                 sample_rate, p, m)

        if "kap" in described_speech:
            print(time.strftime('%H:%M:%S', time.gmtime(i - overlay)), "-------------------------- segment_found")
        else:
            print(time.strftime('%H:%M:%S', time.gmtime(i - overlay)), "--------------------------")
        print(described_speech)

    print("signal translated in:", time.strftime('%H:%M:%S', time.gmtime(time.time() - t1)))


def translate_fragments(times, remove_duplicates, signal, sample_rate):
    """
    This function takes in a list of times, a boolean value, a signal, and a sample rate, and prints a list of translated
    fragments.

    :param times: a list of tuples, each tuple containing the start and end times of a fragment
    :param remove_duplicates: boolean, if True, will remove duplicate fragments
    :param signal: the signal to be translated
    :param sample_rate: the sample rate of the signal
    """
    times = remove_duplicates(times)

    p, m = init_neural_nett()
    t1 = time.time()
    for i in times:
        print(i, "--------------------------")
        print(cz_speech_to_text(signal[(i * sample_rate):((i + 7) * sample_rate)],
                                sample_rate, p, m))
    print("signal translated in:", time.strftime('%H:%M:%S', time.gmtime(time.time() - t1)))


def init_neural_nett():
    """
    It initializes the weights and biases of the neural network.
    """
    processor = Wav2Vec2Processor.from_pretrained("arampacha/wav2vec2-large-xlsr-czech")
    model = Wav2Vec2ForCTC.from_pretrained("arampacha/wav2vec2-large-xlsr-czech")
    return processor, model


def cz_speech_to_text(audio_input, sample_rate, processor, model):
    """
    It takes in an audio signal, converts it to a spectrogram, and then uses a deep learning model to convert that spectrogram
    into a human-readable transcription.

    :param audio_input: the audio file you want to transcribe
    :param sample_rate: The sample rate of the audio input
    :param processor: The processor to use. Either "google" or "ibm"
    :param model: The model to use. Can be 'command_and_search' or 'phone_call'
    """
    inputs = processor(audio_input, sampling_rate=sample_rate,
                       return_tensors="pt", padding=True).input_values

    logits = model(inputs).logits
    predicted_ids = torch.argmax(logits, dim=-1)

    # transcribe
    transcription = processor.decode(predicted_ids[0])
    return transcription
