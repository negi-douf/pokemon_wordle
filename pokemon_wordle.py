# -*- coding: utf-8 -*-

import random
import re
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from enum import Enum, auto

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
        self.round = 0
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
        if type_02 == '':
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

    def print_winner(self):
        pass

    def move_next_turn(self) -> None:
        pass

    def answer_of_this_turn(self) -> str:
        return ''

    def label_yellow(self, answer: str, correct_answer: str) -> list[Color]:
        yellow_labels: list[Color] = []
        count_moji: dict[str, int] = {}
        for c in correct_answer:
            count_moji[c] = correct_answer.count(c)

        for c in answer:
            if c in correct_answer and count_moji[c] > 0:
                yellow_labels.append(Color.YELLOW)
                count_moji[c] -= 1
            else:
                yellow_labels.append(Color.NONE)
        return yellow_labels

    def label_green(self, answer: str, correct_answer: str) -> list[Color]:
        green_labels: list[Color] = [Color.NONE] * 5
        for index, answer_char in enumerate(answer):
            if answer_char == correct_answer[index]:
                green_labels[index] = Color.GREEN
        return green_labels

    def merge_labels(self, yellow_labels: list[Color], green_labels: list[Color]) -> list[Color]:
        color_labels: list[Color] = []
        for yellow_label, green_label in zip(yellow_labels, green_labels):
            if green_label == Color.GREEN:
                color_labels.append(Color.GREEN)
            elif yellow_label == Color.YELLOW:
                color_labels.append(Color.YELLOW)
            else:
                color_labels.append(Color.NONE)
        return color_labels

    def _print_colored_feedback(self, color_labels: list[Color], answer: str) -> None:
        print('  ', end='')
        for index, color_label in enumerate(color_labels):
            if color_label == Color.GREEN:
                print(colorama.Fore.GREEN + answer[index], end='')
            elif color_label == Color.YELLOW:
                print(colorama.Fore.YELLOW + answer[index], end='')
            else:
                print(colorama.Fore.WHITE + '・', end='')
        print()

    def print_colored_feedback(self, answer: str) -> None:
        correct_answer = self.answer_pokemon.name
        yellow_labels = self.label_yellow(answer, correct_answer)
        green_labels = self.label_green(answer, correct_answer)
        color_labels = self.merge_labels(yellow_labels, green_labels)
        self._print_colored_feedback(color_labels, answer)


class SoloPlayGame(Game):
    def __init__(self, answer_pokemon: Pokemon) -> None:
        super().__init__(answer_pokemon)

    def move_next_turn(self) -> None:
        self.round += 1

    def print_winner(self):
        print(f"{self.round}手目で正解！")
        self.finished = True

    def answer_of_this_turn(self) -> str:
        answer_word = input("> ")
        return answer_word


class AI:
    def __init__(self, pokemons: list[Pokemon]) -> None:
        self.answer = ""
        self.pokemons = pokemons

    def think(self) -> None:
        choiced_pokemon = random.choice(self.pokemons)
        self.answer = choiced_pokemon.name


class BattleAIGame(Game):
    def __init__(self, answer_pokemon: Pokemon, ai: AI) -> None:
        super().__init__(answer_pokemon)
        self.ai = ai

    def move_next_turn(self) -> None:
        self.is_players_turn = not self.is_players_turn
        self.round += 1

    def print_winner(self):
        print(f"{self.round}手目で正解！")
        if self.is_players_turn:
            print("プレイヤーの勝利！")
        else:
            print("コンピュータの勝利！")
        self.finished = True

    def answer_of_this_turn(self) -> str:
        if self.is_players_turn:
            answer_word = input("> ")
        else:
            self.ai.think()
            answer_word = self.ai.answer
        return answer_word


def load_pokemons(filepath: str) -> list[Pokemon]:
    with open(filepath, "r", encoding="utf-8") as f:
        reader = DataclassReader(f, Pokemon)
        pokemons = [row for row in reader]
    return pokemons


def choice_pokemon(pokemons: list[Pokemon]) -> Pokemon:
    choiced_pokemon = random.choice(pokemons)
    return choiced_pokemon


def is_invalid_answer(answer: str) -> bool:
    if len(answer) != 5:
        return True

    re_katakana = re.compile(r'[\u30A1-\u30F4ー]+')
    if not re_katakana.fullmatch(answer):
        return True
    return False


def is_system_command(word: str) -> bool:
    if word in [e.value for e in SystemCommand]:
        return True
    return False


def pokemon_wordle(choiced_pokemon: Pokemon, game: Game) -> None:
    while not game.finished:
        answer_word = game.answer_of_this_turn()

        if is_system_command(answer_word):
            game.exec_system_command(answer_word)
            continue

        if is_invalid_answer(answer_word):
            print("回答はカタカナ5文字で入力してください。")
            continue

        if not game.is_players_turn:
            print(f'  {answer_word}')

        if answer_word == choiced_pokemon.name:
            game.print_winner()
        else:
            game.print_colored_feedback(answer_word)
            game.move_next_turn()


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


def arg_parser() -> Namespace:
    parser = ArgumentParser(description="5文字のポケモンの名前を当てるゲームです！")
    parser.add_argument("input_filepath", type=str, help="インポートするポケモンリストのファイルパス")
    parser.add_argument("--debug", action="store_true", help="デバッグモードで実行する")
    parser.add_argument("--vs", action="store_true", help="コンピュータとの対戦モードで実行する")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = arg_parser()
    main(args)
