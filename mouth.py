import requests
import tempfile
import os

import simpleaudio

from util import get_logger


class Mouth():
    def __init__(self) -> None:
        self.logger = get_logger("mouth", "info")

    def speak(self, text: str) -> None:
        self.logger.info(f"spearK {text}")


class VoicevoxMouth(Mouth):
    def __init__(self, speaker_id=43) -> None:
        super().__init__()
        self.speaker_id = speaker_id


    def speak(self, text: str) -> None:
        super().speak(text)
        resp = requests.post(f"http://localhost:50021/audio_query?speaker={self.speaker_id}&text={text}")
        resp = requests.post(f"http://localhost:50021/synthesis?speaker={self.speaker_id}", json=resp.json())
        with tempfile.TemporaryFile(mode='wb', delete=False) as f:
            f.write(resp.content)
        wav_obj = simpleaudio.WaveObject.from_wave_file(f.name)
        play_obj = wav_obj.play()
        play_obj.wait_done()
        os.unlink(f.name)


class PrinterMouth(Mouth):
    def __init__(self) -> None:
        super().__init__()


    def speak(self, text: str) -> None:
        super().speak(text)



def mouth(type: str) -> Mouth:
    if type == "voicevox":
        return VoicevoxMouth()
    if type == "printer":
        return PrinterMouth()
    raise NotImplementedError()



if __name__ == "__main__":
    PrinterMouth().speak("こんにちは")
