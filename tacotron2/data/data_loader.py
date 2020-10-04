# -*- coding: utf-8 -*-
# Soohwan Kim @sooftware
# This source code is licensed under the Apache 2.0 License license found in the
# LICENSE file in the root directory of this source tree

import threading


class TextMelDataset(object):
    def __init__(self):
        pass

    def get_item(self):
        pass


class TextMelDataLoader(threading.Thread):
    def __init__(self, dataset: TextMelDataset, queue, batch_size, thread_id):
        super(TextMelDataLoader, self).__init__()

    def run(self):
        raise NotImplementedError


class MultiDataLoader(object):
    """
    Multi Data Loader using Threads.

    Args:
        dataset_list (list): list of MelSpectrogramDataset
        queue (Queue.queue): queue for threading
        batch_size (int): size of batch
        num_workers (int): the number of cpu cores used
    """
    def __init__(self, dataset_list, queue, batch_size, num_workers):
        self.dataset_list = dataset_list
        self.queue = queue
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.loader = list()

        for idx in range(self.num_workers):
            self.loader.append(TextMelDataLoader(self.dataset_list[idx], self.queue, self.batch_size, idx))

    def start(self):
        """ Run threads """
        for idx in range(self.num_workers):
            self.loader[idx].start()

    def join(self):
        """ Wait for the other threads """
        for idx in range(self.num_workers):
            self.loader[idx].join()


def load_dataset(filepath: str, separator: str = '|'):
    audio_paths = list()
    transcripts = list()

    with open(filepath) as f:
        for line in f.readlines():
            audio_path, transcript, _ = line.split(separator)
            audio_paths.append(audio_path)
            transcripts.append(transcript)

    return audio_paths, transcripts
