# -*- coding: utf-8 -*-

import random
import re
from argparse import ArgumentParser, Namespace
from collections import Counter
from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterable

import colorama
from dataclass_csv import DataclassReader


@dataclass
class Pokemon:
    name: str
    type_01: str
    type_02: str = ""


class SystemCommand(Enum):
    HELP = "help"
    QUIT = "quit"
    HINT = "hint"


class Color(Enum):
    GREEN = auto()
    YELLOW = auto()
    NONE = auto()


class Game():
    def __init__(self, answer_pokemon: Pokemon) -> None:
        self.round = 1
        self.is_players_turn = True
        self.is_first_hint = True
        self.answer_pokemon = answer_pokemon
        self.finished = False
        self.print_instructions()
        colorama.init(autoreset=True)

    def print_instructions(self) -> None:
        print("help: ゲームのルールを表示")
        print("hint: タイプのヒントを表示")
        print("quit: 終了\n")

    def print_hint(self) -> None:
        type_01 = self.answer_pokemon.type_01
        type_02 = self.answer_pokemon.type_02
        if type_02 == "":
            type_02 = "なし"

        if self.is_first_hint:
            print(f"type_01: {type_01}\n".format(type_01))
            self.is_first_hint = False
        else:
            print(f"type_01: {type_01}, type_02: {type_02}\n")

    def print_help(self) -> None:
        print("5文字のポケモンの名前を当てるゲームです！\n")
        print(colorama.Fore.YELLOW + "文字だけ合っていたら黄色で、")
        print(colorama.Fore.GREEN + "文字も位置も合っていたら緑色で、")
        print(colorama.Fore.WHITE + "違っていたら白色の \"・\" で表示します。\n")

    def quit(self) -> None:
        print(f"正解は{self.answer_pokemon.name}でした。")
        self.finished = True

    def exec_system_command(self, word: str) -> None:
        if word == SystemCommand.QUIT.value:
            self.quit()
        elif word == SystemCommand.HELP.value:
            self.print_help()
        elif word == SystemCommand.HINT.value:
            self.print_hint()

    def print_winner(self) -> None:
        pass

    def move_to_next_turn(self) -> None:
        pass

    def response_of_this_turn(self) -> str:
        return ""

    def label(self, response: str) -> list[Color]:
        answer = self.answer_pokemon.name
        labels: list[Color] = []

        answer_counter = Counter(answer)
        response_counter = Counter(response)
        char_set_intersection = set(list(response)) & set(list(answer))
        need_to_label_list: list[str] = []
        for char in char_set_intersection:
            for _ in range(min(response_counter[char], answer_counter[char])):
                need_to_label_list.append(char)

        for response_char, answer_char in zip(response, answer):
            if response_char not in need_to_label_list:
                labels.append(Color.NONE)
            elif response_char == answer_char:
                labels.append(Color.GREEN)
                need_to_label_list.remove(response_char)
            else:
                labels.append(Color.YELLOW)
                need_to_label_list.remove(response_char)

        return labels

    def _print_colored_feedback(self, color_labels: list[Color], response: str) -> None:
        print("  ", end="")
        for index, color_label in enumerate(color_labels):
            if color_label == Color.GREEN:
                print(colorama.Fore.GREEN + response[index], end="")
            elif color_label == Color.YELLOW:
                print(colorama.Fore.YELLOW + response[index], end="")
            else:
                print(colorama.Fore.WHITE + "・", end="")
        print()

    def print_colored_feedback(self, response: str) -> None:
        color_labels = self.label(response)
        self._print_colored_feedback(color_labels, response)


class SoloPlayGame(Game):
    def __init__(self, answer_pokemon: Pokemon) -> None:
        super().__init__(answer_pokemon)

    def move_to_next_turn(self) -> None:
        self.round += 1

    def print_winner(self) -> None:
        print(f"{self.round}手目で正解！")
        self.finished = True

    def response_of_this_turn(self) -> str:
        response_word = input("> ")
        return response_word


class AI:
    def __init__(self, pokemons: list[Pokemon]) -> None:
        self.response = ""
        self.pokemons = pokemons

    def think(self) -> None:
        choiced_pokemon = random.choice(self.pokemons)
        self.response = choiced_pokemon.name


class BattleAIGame(Game):
    def __init__(self, answer_pokemon: Pokemon, ai: AI) -> None:
        super().__init__(answer_pokemon)
        self.ai = ai

    def move_to_next_turn(self) -> None:
        self.is_players_turn = not self.is_players_turn
        self.round += 1

    def print_winner(self) -> None:
        print(f"{self.round}手目で正解！")
        if self.is_players_turn:
            print("プレイヤーの勝利！")
        else:
            print("コンピュータの勝利！")
        self.finished = True

    def response_of_this_turn(self) -> str:
        if self.is_players_turn:
            response_word = input("> ")
        else:
            self.ai.think()
            response_word = self.ai.response
        return response_word


def load_pokemons(filepath: str) -> list[Pokemon]:
    with open(filepath, "r", encoding="utf-8") as f:
        reader: Iterable[Pokemon] = DataclassReader(f, Pokemon)
        pokemons = [row for row in reader]
    return pokemons


def choice_pokemon(pokemons: list[Pokemon]) -> Pokemon:
    choiced_pokemon = random.choice(pokemons)
    return choiced_pokemon


def is_invalid_response(response: str) -> bool:
    if len(response) != 5:
        return True

    re_katakana = re.compile(r"[\u30A1-\u30F4ー]+")
    if not re_katakana.fullmatch(response):
        return True
    return False


def is_system_command(word: str) -> bool:
    if word in [e.value for e in SystemCommand]:
        return True
    return False


def pokemon_wordle(answer_pokemon: Pokemon, game: Game) -> None:
    while not game.finished:
        response_word = game.response_of_this_turn()

        if is_system_command(response_word):
            game.exec_system_command(response_word)
            continue

        if is_invalid_response(response_word):
            print("回答はカタカナ5文字で入力してください。")
            continue

        if not game.is_players_turn:
            print(f"  {response_word}")

        if response_word == answer_pokemon.name:
            game.print_winner()
        else:
            game.print_colored_feedback(response_word)
            game.move_to_next_turn()


def main(args: Namespace) -> None:
    filepath: str = args.input_filepath
    is_debug: bool = args.debug
    is_vs: bool = args.vs
    game: Game

    pokemons = load_pokemons(filepath)
    choiced_pokemon = choice_pokemon(pokemons)

    if is_debug:
        print(choiced_pokemon)

    if is_vs:
        ai = AI(pokemons)
        game = BattleAIGame(choiced_pokemon, ai)
    else:
        game = SoloPlayGame(choiced_pokemon)

    pokemon_wordle(choiced_pokemon, game)


def parse_args() -> Namespace:
    parser = ArgumentParser(description="5文字のポケモンの名前を当てるゲームです！")
    parser.add_argument("input_filepath", type=str, help="インポートするポケモンリストのファイルパス")
    parser.add_argument("--debug", action="store_true", help="デバッグモードで実行する")
    parser.add_argument("--vs", action="store_true", help="コンピュータとの対戦モードで実行する")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    main(args)
