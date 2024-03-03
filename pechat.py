import os

from ear import Ear
from brain import Brain
from recognizer import recognizer
from mouth import mouth
from util import get_logger


logger = get_logger(__name__)


class Pechat:
    def __init__(self, recognize_type: str, mouth_type: str) -> None:
        self.ear = Ear(recognaizer=recognizer(recognize_type))
        self.brain = Brain(os.environ.get("OPENAI_API_KEY"))
        self.mouth = mouth(mouth_type)

    def __process(self, text):
        logger.info(f"user: {text}")
        reply = self.brain.reply(text=text)
        logger.info(f"pechat: {reply}")
        self.mouth.speak(reply)

    def start(self):
        logger.info("Starting...")
        self.ear.listen(self.__process)
