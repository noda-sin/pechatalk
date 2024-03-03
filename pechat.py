import os

from ear import Ear
from brain import Brain
from recognizer import recognizer
from mouth import mouth
from util import get_logger


class Pechat:
    def __init__(self, recognize_type: str, mouth_type: str) -> None:
        self.logger = get_logger("Pechat", "info")
        self.ear = Ear(recognaizer=recognizer(recognize_type))
        self.brain = Brain(os.environ.get("OPENAI_API_KEY"))
        self.mouth = mouth(mouth_type)
    

    def __process(self, text):
        self.logger.info(f"user: {text}")
        reply = self.brain.reply(text=text)
        self.logger.info(f"pechat: {reply}")
        self.mouth.speak(reply)


    def start(self):
        self.logger.info("Starting...")
        self.ear.listen(self.__process)
