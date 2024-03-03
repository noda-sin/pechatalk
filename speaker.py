
import requests
import tempfile
import os

import simpleaudio

class Speaker:
    def __init__(self, speaker_id=43) -> None:
        self.speaker_id = speaker_id


    def speak(self, text: str):
        resp = requests.post(f"http://localhost:50021/audio_query?speaker={self.speaker_id}&text={text}")
        resp = requests.post(f"http://localhost:50021/synthesis?speaker={self.speaker_id}", json=resp.json())
        with tempfile.TemporaryFile(mode='wb', delete=False) as f:
            f.write(resp.content)
        wav_obj = simpleaudio.WaveObject.from_wave_file(f.name)
        play_obj = wav_obj.play()
        play_obj.wait_done()
        os.unlink(f.name)


if __name__ == "__main__":
    Speaker().speak("こんにちは")
