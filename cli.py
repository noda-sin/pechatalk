#!/usr/bin/env python3

import os
import click

from pechat import Pechat


@click.command()
@click.option("--apikey", default=os.environ.get("OPENAI_API_KEY"), type=str)
@click.option("--recognizer", default="reazon_speech", type=str)
@click.option("--mouth", default="printer", type=str)
def main(apikey: str, recognizer: str, mouth: str) -> None:
    try:
        bot = Pechat(openai_api_key=apikey, recognize_type=recognizer, mouth_type=mouth)
        bot.start()
    except KeyboardInterrupt:
        print("Operation interrupted successfully")


if __name__ == "__main__":
    main()
