import abc
import os

import torch
from util import get_logger


logger = get_logger(__name__)


class Recognizer(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def recognize(self, audio_data, samplerate) -> str:
        raise NotImplementedError()

class FasterWhisperRecognizer(Recognizer):
    def __init__(
        self,
        model="large-v3",
        device=("cuda" if torch.cuda.is_available() else "cpu"),
        model_root="~/.cache/whisper",
    ) -> None:
        logger.info(f"Recognizer device: {device}")

        from faster_whisper import WhisperModel

        model_root = os.path.expanduser(model_root)
        self.model = WhisperModel(
            model, download_root=model_root, device=device, compute_type="int8"
        )

    def recognize(self, audio_data, samplerate) -> str:
        predicted_text = ""
        segments, _ = self.model.transcribe(audio_data)
        for segment in segments:
            predicted_text += segment.text
        return predicted_text


def recognizer(type: str) -> Recognizer:
    logger.info(f"Recognizer: {type}")

    if type == "faster_wisper":
        return FasterWhisperRecognizer()
    raise NotImplementedError()
