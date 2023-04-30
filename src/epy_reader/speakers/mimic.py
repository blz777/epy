import shutil
import subprocess
import threading

from epy_reader.speakers.base import SpeakerBaseModel


class SpeakerMimic(SpeakerBaseModel):
    cmd = "mimic3"
    available = bool(shutil.which("mimic3"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.audio_done = threading.Event()

    def speak(self, text: str):
        self.audio_done.clear()

        self.mimic3_process = subprocess.Popen(
            [self.cmd, *self.args],
            text=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )

        self.process = subprocess.Popen(
            ["play", "-t", "wav", "-"],
            stdin=self.mimic3_process.stdout,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        self.mimic3_process.stdin.write(text)
        self.mimic3_process.stdin.close()

        self.wait_for_audio()

    def wait_for_audio(self):
        self.process.wait()
        self.audio_done.set()

    def is_done(self) -> bool:
        return self.audio_done.is_set()

    def stop(self) -> None:
        self.process.terminate()

    def cleanup(self) -> None:
        pass
