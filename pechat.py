import queue

from ear import Ear
from brain import Brain
from recognizer import recognizer
from mouth import mouth
from util import get_logger


logger = get_logger(__name__)


class Pechat:
    def __init__(self, openai_api_key: str, recognize_type: str, mouth_type: str) -> None:
        self.ear = Ear(recognaizer=recognizer(recognize_type))
        self.brain = Brain(openai_api_key)
        self.mouth = mouth(mouth_type)

        self.messages = []
        self.is_speaking = False

    def __process(self, text):
        self.messages.append(text)
        if self.is_speaking:
            return

        self.is_speaking = True
        messages = self.messages
        self.messages = []

        if len(messages) == 0:
            return

        message = " ".join(messages)

        try:
            logger.info(f"user: {message}")
            reply = self.brain.reply(text=message)
            logger.info(f"pechat: {reply}")
            self.mouth.speak(reply)
        finally:
            self.is_speaking = False


    def start(self):
        logger.info("Starting...")
        self.ear.listen(self.__process)
