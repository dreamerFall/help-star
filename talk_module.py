"""i had a fight with python pip pakage (important)
first of all in 'speech_recognition' there was no function named
'recognize_google()' so i needed to download speech to text module
at first my idea was to install "google-cloud-speech" but it didn't installed
what about "openai-wisper" you mght ask?... didn't installed either
nothing...but i find a way and that was using 'vosk'
and yeah that why i used extra module"""

"""another problem i can't install piper(is a text-to-speech module)
so we still gomma use pyttsx3"""
import wave, pyttsx3
import vosk
from tools.jokes import joke
from json import load, loads, dump, JSONDecodeError
from os import name, system, path
from colorama import Fore, init
from time import sleep
from vosk import Model, KaldiRecognizer, SetLogLevel
from speech_recognition import Recognizer, Microphone
from playsound3 import playsound, PlaysoundException


# fix: vosk Model.__del__ crashes if Ctrl+C interrupts __init__
_original_del = vosk.Model.__del__


def _safe_del(self):
    if hasattr(self, "_handle"):
        _original_del(self)


vosk.Model.__del__ = _safe_del


def clear():
    if name == "nt":
        system("cls")
    else:
        system("clear")


class JsonStart:
    def __init__(self):
        with open("data.json", "r") as file:
            self.data = load(file)


class Hear(JsonStart):
    def __init__(self):
        super().__init__()
        print("load")
        SetLogLevel(-1)
        self.the_model = self.data["model"]
        self.model = Model(path.abspath(self.the_model))

    def start(
        self,
    ):
        r = Recognizer()
        try:
            playsound(path.abspath("sfx/input.wav"), block=False)
        except FileNotFoundError:
            pass
        except PlaysoundException:
            pass
        print(Fore.LIGHTRED_EX + "recording...")
        with Microphone() as source:
            audio = r.listen(source)
        with open("audio_user.wav", "wb") as wav_get:
            wav_get.write(audio.get_wav_data())
        # text to speech

        wf = wave.open(path.abspath("audio_user.wav"), "rb")
        rec = KaldiRecognizer(self.model, wf.getframerate())
        result_text = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = loads(rec.Result())
                result_text.append(result.get("text", ""))
        final_result = loads(rec.FinalResult())
        result_text.append(final_result.get("text", ""))
        full_transcript = " ".join(result_text).strip()
        nothing_catcher = full_transcript
        nothing_catcher = nothing_catcher.replace(" ", "")
        print(Fore.GREEN, end="")
        if nothing_catcher == "":
            print("...")
        else:
            print(full_transcript)
        print(Fore.RESET, end="")
        try:
            playsound(path.abspath("sfx/output.wav"))
        except FileNotFoundError:
            sleep(0.75)
        except PlaysoundException:
            sleep(0.75)
        return full_transcript


class Speak(JsonStart):
    def __init__(self):
        super().__init__()
        init()
        if self.data["init-push"] == False:
            self.run = pyttsx3.init()
            self.run.setProperty("rate", self.data["speech-rate"])
            self.run.setProperty("volume", self.data["speech-volume"])

    def start(self, speech, text=None):
        if text == None:
            text = speech
        print(text)
        if self.data["init-push"] == False:
            self.run.say(speech)
            self.run.runAndWait()
        else:
            pyttsx3.speak(speech)