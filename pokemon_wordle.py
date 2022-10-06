# -*- coding: utf-8 -*-

import random
import re
from argparse import ArgumentParser, Namespace
from collections import Counter
from dataclasses import dataclass
from enum import Enum
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
    GREEN = colorama.Fore.GREEN
    YELLOW = colorama.Fore.YELLOW
    WHITE = colorama.Fore.WHITE


class ColorLabels:
    def __init__(self, answer: str, response: str) -> None:
        self.answer = answer
        self.response = response
        self.labels = self._get_color_labels()

    def _get_need_to_label_list(self) -> list[str]:
        answer = self.answer
        response = self.response
        answer_counter = Counter(answer)
        response_counter = Counter(response)
        char_set_intersection = set(list(response)) & set(list(answer))

        need_to_label_list: list[str] = []
        for char in char_set_intersection:
            for _ in range(min(response_counter[char], answer_counter[char])):
                need_to_label_list.append(char)
        return need_to_label_list

    def _get_color_labels(self) -> list[Color]:
        answer = self.answer
        response = self.response
        labels: list[Color] = [Color.WHITE] * 5
        need_to_label_list = self._get_need_to_label_list()

        for index, (response_char, answer_char) in enumerate(zip(response, answer)):
            if response_char == answer_char:
                labels[index] = Color.GREEN
                need_to_label_list.remove(response_char)

        for index, (response_char, answer_char) in enumerate(zip(response, answer)):
            if labels[index] != Color.GREEN and response_char in need_to_label_list:
                labels[index] = Color.YELLOW
                need_to_label_list.remove(response_char)
        return labels

    @property
    def feedback_str(self) -> str:
        labels = self.labels
        response = self.response
        feedback_str: str = "  "
        for label, response_char in zip(labels, response):
            if label == Color.WHITE:
                response_char = "・"
            feedback_str += label.value + response_char
        feedback_str += "\n"
        return feedback_str


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

    def is_invalid_response(self, response: str) -> bool:
        if len(response) != 5:
            return True

        re_katakana = re.compile(r"[\u30A1-\u30F4ー]+")
        if not re_katakana.fullmatch(response):
            return True
        return False

    def is_system_command(self, word: str) -> bool:
        if word in [e.value for e in SystemCommand]:
            return True
        return False

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

    def print_colored_feedback(self, response: str) -> None:
        color_labels = ColorLabels(self.answer_pokemon.name, response)
        print(color_labels.feedback_str)


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


def pokemon_wordle(answer_pokemon: Pokemon, game: Game) -> None:
    while not game.finished:
        response_word = game.response_of_this_turn()

        if game.is_system_command(response_word):
            game.exec_system_command(response_word)
            continue

        if game.is_invalid_response(response_word):
            print("回答はカタカナ5文字で入力してください。")
            continue

        if not game.is_players_turn:
            print(f"  {response_word}")

        if response_word == answer_pokemon.name:
            game.print_winner()
        else:
            game.print_colored_feedback(response_word)
            game.move_to_next_turn()


def parse_args() -> Namespace:
    parser = ArgumentParser(description="5文字のポケモンの名前を当てるゲームです！")
    parser.add_argument("input_filepath", type=str, help="インポートするポケモンリストのファイルパス")
    parser.add_argument("--debug", action="store_true", help="デバッグモードで実行する")
    parser.add_argument("--vs", action="store_true", help="コンピュータとの対戦モードで実行する")
    args = parser.parse_args()
    return args


def main() -> None:
    args = parse_args()
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


if __name__ == "__main__":
    main()
