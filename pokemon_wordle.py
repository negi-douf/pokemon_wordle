# -*- coding: utf-8 -*-

import random
import re
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from enum import Enum

from colorama import Fore
from colorama import init as colorama_init
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
        

class Game():
    def __init__(self, answer_pokemon: Pokemon) -> None:
        self.round= 0
        self.is_first_hint = True
        self.answer_pokemon = answer_pokemon
        self.finished = False
        self.print_instructions()
        colorama_init(autoreset=True)

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
        print(Fore.YELLOW + "文字だけ合っていたら黄色で、")
        print(Fore.GREEN + "文字も位置も合っていたら緑色で、")
        print(Fore.WHITE + "違っていたら白色の \"・\" で表示します。\n")

    def quit(self) -> None:
        print(f"正解は{self.answer_pokemon.name}でした。")
        self.finished = True

    def exec_systemcommand(self, word: str) -> None:
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

    def is_green_match(self,answer_char: str,index: int) -> bool:
        pokemon_name = self.answer_pokemon.name
        if pokemon_name[index] == answer_char:
            return True
        return False
    
    def is_yellow_match(self,answer_char: str) -> bool:
        pokemon_name = self.answer_pokemon.name
        if re.search(answer_char,pokemon_name):
            return True
        return False
    
    def print_colored_feedback_per_char(self,char: str,index: int) -> None:
        if self.is_green_match(char,index):
            print(Fore.GREEN + char, end='')
        elif self.is_yellow_match(char):
            print(Fore.YELLOW + char, end='')
        else:
            print(Fore.WHITE + char, end='')

    def print_colored_feedback(self, answer: str) -> None:
        pokemon_name = self.answer_pokemon.name
        if len(pokemon_name) != len(answer):
            raise ValueError("targetとanswerの文字数が一致しません。")

        for index,answer_char in enumerate(answer):
            self.print_colored_feedback_per_char(answer_char,index)
        print()


class Game_VS_SELF(Game):
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


class Game_VS_AI(Game):
    def __init__(self, answer_pokemon: Pokemon, ai: AI) -> None:
        super().__init__(answer_pokemon)
        self.is_player_turn = True
        self.ai = ai

    def move_next_turn(self) -> None:
        self.is_player_turn = not self.is_player_turn
        self.round += 1

    def print_winner(self):
        print(f"{self.round}手目で正解！")
        if self.is_player_turn:
            print("コンピュータの勝利！")
        else:
            print("プレイヤーの勝利！")
        self.finished = True

    def answer_of_this_turn(self) -> str:
        if self.is_player_turn:
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


def is_systemcommand(word: str) -> bool:
    if word in [e.value for e in SystemCommand]:
        return True
    return False


def pokemon_wordle(choiced_pokemon: Pokemon, game: Game) -> None:
    while not game.finished:
        answer_word = game.answer_of_this_turn()

        if is_systemcommand(answer_word):
            game.exec_systemcommand(answer_word)
            continue

        if is_invalid_answer(answer_word):
            print("回答はカタカナ5文字で入力してください。")
            continue

        if answer_word == choiced_pokemon.name:
            game.print_winner()
        else:
            game.print_colored_feedback(answer_word)
            game.move_next_turn()


def main(args: Namespace) -> None:
    filepath: str = args.list
    is_debug: bool = args.debug
    is_vs: bool = args.vs

    pokemons = load_pokemons(filepath)
    choiced_pokemon = choice_pokemon(pokemons)

    if is_debug:
        print(choiced_pokemon)

    if is_vs:
        ai = AI(pokemons)
        game = Game_VS_AI(choiced_pokemon, ai)
    else:
        game = Game_VS_SELF(choiced_pokemon)

    pokemon_wordle(choiced_pokemon, game)


def arg_parser() -> Namespace:
    parser = ArgumentParser(description="5文字のポケモンの名前を当てるゲームです！")
    parser.add_argument("list", type=str, help="ポケモンのリスト (csvファイルのパス)")
    parser.add_argument("--debug", action="store_true", help="デバッグモードで実行する")
    parser.add_argument("--vs", action="store_true", help="コンピュータとの対戦モードで実行する")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = arg_parser()
    main(args)
