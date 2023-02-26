import time

import ffmpeg
import numpy as np


def time_to_sec(time: str):
    """
    :param time: "hh:mm:ss"
    :return: seconds
    """
    time = time.split(":")
    return 3600 * int(time[0]) + 60 * int(time[1]) + int(time[2])


def remove_duplicates(times):
    # removes duplicate records
    tmp = []
    for t in times:
        if len(tmp) > 0 and time_to_sec(t) - tmp[-1] < 15:
            continue
        tmp.append(time_to_sec(t))
    return tmp


def work_butcher(file_name, times):
    """
    This function takes a file name and a list of times and cut file into defined segments.
    for each time in the list.

    :param file_name: the name of the file you want to butcher
    :param times: the number of times you want to run the program
    """
    name = file_name.split("/")
    for i in range(len(times)):
        j = i + 1
        if i == len(times) - 1:
            j = -1
        audio_cut = ffmpeg.input(file_name, ss=time_to_sec(times[i]),
                                 t=time_to_sec(times[j]) - time_to_sec(times[i]))
        audio_output = ffmpeg.output(audio_cut, "./" + str(i) + "_" + name[-1])
        ffmpeg.run(audio_output, capture_stdout=True)


def cut_times_from_file(file_name):
    """
    This function takes a file name as input and cut file into defined segments.

    :param file_name: the name of the file to read from
    """
    with open("notes/out2.txt") as f:
        times = f.readlines()
    times = [x.strip() for x in times]
    work_butcher(file_name, times)


def normalize_signal(input_signal: np.ndarray) -> np.ndarray:
    """
    > This function takes in a signal and returns a normalized version of it

    :param input_signal: The input signal to be normalized
    :type input_signal: np.ndarray
    """
    signal_mean = np.mean(input_signal, axis=0)
    signal_std = np.std(input_signal, axis=0)
    return (input_signal - signal_mean) / signal_std


def show_few_bests(stats: dict, min: int):
    """
    It takes a dictionary of stats and a minimum value, and returns a list of the keys in the dictionary whose values are
    greater than or equal to the minimum

    :param stats: a dictionary of the form {'name': [score, score, score, ...], ...}
    :type stats: dict
    :param min: the minimum number of times a word must appear in the corpus to be considered
    :type min: int
    """
    results = []
    res = {key: val for key, val in sorted(stats.items(), key=lambda ele: ele[0])}
    for index, i in enumerate(res):
        if index < min:
            for j in res[i]:
                results.append(j)
    results.sort()
    for i in results:
        print(
            time.strftime('%H:%M:%S', time.gmtime(i))
        )


def add_to_stats_dictionary(stats_dict, key, value):
    """
    It adds a key-value pair to a dictionary

    :param stats_dict: a dictionary of dictionaries
    :param key: The key to add to the dictionary
    :param value: the value to add to the dictionary
    """
    if key not in stats_dict.keys():
        stats_dict[key] = [value]
    else:
        stats_dict[key].append(value)
    return stats_dict
