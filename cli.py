#!/usr/bin/env python3

import click

from pechat import Pechat


@click.command()
@click.option("--recognizer", default="reazon_speech", type=str)
@click.option("--mouth", default="printer", type=str)
def main(recognizer: str, mouth: str) -> None:
    try:
        bot = Pechat(recognize_type=recognizer, mouth_type=mouth)
        bot.start()
    except KeyboardInterrupt:
        print("Operation interrupted successfully")


if __name__ == "__main__":
    main()
