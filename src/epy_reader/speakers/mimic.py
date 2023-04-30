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
            [self.cmd, *self.args, "--interactive"],
            text=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )

        self.process = subprocess.Popen(
            ["play", "-t", "wav", "-"],
            stdin=self.mimic3_process.stdout,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        self.mimic3_process.stdin.write(text)
        self.mimic3_process.stdin.close()

        threading.Thread(target=self.wait_for_audio, daemon=True).start()

    def wait_for_audio(self):
        self.process.wait()
        self.mimic3_process.wait()
        self.audio_done.set()

    def is_done(self) -> bool:
        return self.audio_done.is_set()

    def stop(self) -> None:
        self.process.terminate()
        self.mimic3_process.terminate()

    def cleanup(self) -> None:
        pass
