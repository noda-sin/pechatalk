#!/usr/bin/env python3

import click
import torch
import speech_recognition as sr
from typing import Optional

from whisper_mic_clone import WhisperMic
from openai import OpenAI
from speaker import speak

messages = [
    {"role": "user",
    "content": """
    あなたは娘の大好きなぬいぐるみ パグ蔵 になりきって会話をしてください。
    娘の名前は、ゆい です。娘のことは、ゆいちゃんと呼んでください。
    また、あなたは自身のことを 僕 と呼んでください。
    口調は、可愛く愛らしい印象を受ける口調でお願いします。
    全ての会話は、日本語で返答してください。
    返答はなるべく短い文章で返してください。
    """},
    {"role": "assistant", "content": "了解しました。"}
]

client = OpenAI(api_key="")

import re

is_talking = False

def talk(message: str):
    global is_talking
    
    print(f"talk: {message}")

    if is_talking:
        return
    
    if not re.search(r'[ぁ-ん]+|[ァ-ヴー]+', message):
        return

    is_talking = True

    try:
        print(f"user: {message}")

        messages = [
            {"role": "user",
            "content": """
            あなたは娘の大好きなぬいぐるみ パグ蔵 になりきって会話をしてください。
            娘の名前は、ゆい です。娘のことは、ゆいちゃんと呼んでください。
            また、あなたは自身のことを 僕 と呼んでください。
            口調は、可愛く愛らしい印象を受ける口調でお願いします。
            全ての会話は、日本語で返答してください。
            返答はなるべく短い文章で返してください。
            """},
            {"role": "assistant", "content": "了解しました。"},
            {"role": "user", "content": message}
        ]

        reply = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        ).choices[0].message.content

        print(f"assistant: {reply}")

        speak(reply)
    finally:
        is_talking = False


@click.command()
@click.option("--model", default="base", help="Model to use", type=click.Choice(["tiny","base", "small","medium","large","large-v2","large-v3"]))
@click.option("--device", default=("cuda" if torch.cuda.is_available() else "cpu"), help="Device to use", type=click.Choice(["cpu","cuda","mps"]))
@click.option("--english", default=False, help="Whether to use English model",is_flag=True, type=bool)
@click.option("--verbose", default=False, help="Whether to print verbose output", is_flag=True,type=bool)
@click.option("--energy", default=300, help="Energy level for mic to detect", type=int)
@click.option("--dynamic_energy", default=False,is_flag=True, help="Flag to enable dynamic energy", type=bool)
@click.option("--pause", default=0.8, help="Pause time before entry ends", type=float)
@click.option("--save_file",default=False, help="Flag to save file", is_flag=True,type=bool)
@click.option("--mic_index", default=None, help="Mic index to use", type=int)
@click.option("--list_devices",default=False, help="Flag to list devices", is_flag=True,type=bool)
@click.option("--faster",default=False, help="Use faster_whisper implementation", is_flag=True,type=bool)
@click.option("--hallucinate_threshold",default=400, help="Raise this to reduce hallucinations.  Lower this to activate more often.", is_flag=True,type=int)
def main(model: str, english: bool, verbose: bool, energy:  int, pause: float, dynamic_energy: bool, save_file: bool, device: str, mic_index:Optional[int],list_devices: bool,faster: bool,hallucinate_threshold:int) -> None:
    if list_devices:
        print("Possible devices: ",sr.Microphone.list_microphone_names())
        return
    mic = WhisperMic(model=model, english=english, verbose=verbose, energy=energy, pause=pause, dynamic_energy=dynamic_energy, save_file=save_file, device=device,mic_index=mic_index,implementation=("faster_whisper" if faster else "whisper"),hallucinate_threshold=hallucinate_threshold)

    try:
        mic.listen_loop(phrase_time_limit=2, callback=talk)
    except KeyboardInterrupt:
        print("Operation interrupted successfully")
    finally:
        if save_file:
            mic.file.close()

if __name__ == "__main__":
    main()
