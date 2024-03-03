import queue
import threading
import time
import numpy as np

import speech_recognition as sr

from util import get_logger
from recognizer import Recognizer, ReazonSpeechRecognizer


def to_nparray(data):
    return np.frombuffer(data, np.int16).flatten().astype(np.float32) / 32768.0


class Ear:
    def __init__(self, recognaizer: Recognizer, samplerate=16000):
        self.logger = get_logger("Ear", "info")

        self.samplerate = samplerate
        self.source = sr.Microphone(sample_rate=samplerate)
        self.recorder = sr.Recognizer()
        self.recorder.energy_threshold = 300
        self.recorder.phrase_threshold = 2
        self.recorder.dynamic_energy_threshold = False
        self.hallucinate_threshold = 300

        self.recognizer = recognaizer

        with self.source:
            self.recorder.adjust_for_ambient_noise(self.source)

        self.logger.info("Mic setup complete")

        self.audio_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.intercept = False
    

    def __record_load(self, _, audio: sr.AudioData) -> None:
        data = audio.get_raw_data()
        self.audio_queue.put_nowait(data)


    def __get_all_audio(self, min_time: float = -1.):
        audio = bytes()
        got_audio = False
        time_start = time.time()
        while not got_audio or time.time() - time_start < min_time:
            while not self.audio_queue.empty():
                audio += self.audio_queue.get()
                got_audio = True

        data = sr.AudioData(audio, self.samplerate, 2)
        data = data.get_raw_data()
        return data


    def __is_audio_loud_enough(self, frame):
        audio_frame = np.frombuffer(frame, dtype=np.int16)
        amplitude = np.mean(np.abs(audio_frame))
        return amplitude > self.hallucinate_threshold


    def __transcribe(self):
        audio_data = self.__get_all_audio()
        if not self.__is_audio_loud_enough(audio_data):
            return
        ret = self.recognizer.recognize(to_nparray(audio_data), self.samplerate)
        self.result_queue.put_nowait(ret)


    def __transcribe_loop(self):
        while True:
            self.__transcribe()


    def __listen(self):
        self.logger.info("Listening...")

        self.recorder.listen_in_background(self.source, self.__record_load)
        threading.Thread(target=self.__transcribe_loop, daemon=True).start()

        while True:
            yield self.result_queue.get()


    def listen(self, callback=None):
        for result in self.__listen():
            if callback:
              callback(result)  


def listen_audio(text):
    print(f"listen: {text}")


if __name__ == "__main__":
    recognizer = ReazonSpeechRecognizer()
    mic = Ear(recognaizer=recognizer)
    mic.listen(listen_audio)
