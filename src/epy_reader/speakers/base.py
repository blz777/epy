from typing import List


class SpeakerBaseModel:
    cmd: str = "tts_engine_binary"
    available: bool = False

    def __init__(self, args: List[str] = []):
        self.args = args

    def speak(self, text: str) -> None:
        raise NotImplementedError("Speaker.speak() not implemented")

    def speak_paced(self, text: str, pace=0):
        if pace == 1:
            self.args = ["--length-scale", "0.75"]
            self.speak(text)
            pass
        elif pace == 2:
            self.args = ["--length-scale", "0.5"]
            self.speak(text)
        else:
            self.speak(text)

    def is_done(self) -> bool:
        raise NotImplementedError("Speaker.is_done() not implemented")

    def stop(self) -> None:
        raise NotImplementedError("Speaker.stop() not implemented")

    def cleanup(self) -> None:
        raise NotImplementedError("Speaker.cleanup() not implemented")
