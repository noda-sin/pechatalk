
import requests
import tempfile
import os

import simpleaudio

def speak(text: str, speaker=43):
    resp = requests.post(f"http://localhost:50021/audio_query?speaker={speaker}&text={text}")
    resp = requests.post(f"http://localhost:50021/synthesis?speaker={speaker}", json=resp.json())
    with tempfile.TemporaryFile(mode='wb', delete=False) as f:
        f.write(resp.content)
    wav_obj = simpleaudio.WaveObject.from_wave_file(f.name)
    play_obj = wav_obj.play()
    play_obj.wait_done()
    os.unlink(f.name)

if __name__ == "__main__":
    speak("こんにちは")
