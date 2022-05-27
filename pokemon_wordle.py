# -*- coding: utf-8 -*-

import random
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from typing import Any

import colorama as cl
from dataclass_csv import DataclassReader


@dataclass
class Pokemon:
    name: str
    type_01: str
    type_02: str = ""


def guide():
    """Display a guide.
    ゲームのルールを表示する。
    """
    print("5文字のポケモンの名前を当てるゲームです！\n")
    print(cl.Fore.YELLOW + "文字だけ合っていたら黄色で、")
    print(cl.Fore.GREEN + "文字も位置も合っていたら緑色で、")
    print(cl.Fore.WHITE + "違っていたら白色の \"・\" で表示します。\n")


def hint(pokemon: Pokemon, is_first_hint: bool):
    """Display hints.
    ヒントを表示する。

    Args:
        target (dict): 正解のポケモンの情報
        is_first_hint (bool): 1回目のヒントかどうか
    """
    type_01 = pokemon.type_01
    type_02 = pokemon.type_02
    if pokemon.type_02 == '':
        type_02 = "なし"

    if is_first_hint:
        print("type_01: {}\n".format(type_01))
    else:
        print("type_01: {}, type_02: {}\n".format(type_01, type_02))


def judge(pokemon_name:str, answer:str) -> None:
    """Judge if the answer is correct.
    文字列が正解かどうかを判定し、結果を色付きで出力する。

    Args:
        target (str): 正解の文字列
        answer (str): 回答

    Raises:
        ValueError: targetとanswerの文字数が異なる場合
    """
    if len(pokemon_name) != len(answer):
        raise ValueError("targetとanswerの文字数が一致しません。")

    remaining: list[str] = []
    for c in pokemon_name:
        remaining.append(c)

    is_green_list, remaining = detect_greens(pokemon_name, answer)
    is_yellow_list = detect_yellows(remaining, answer, is_green_list)

    print("  ", end="")
    for i, c in enumerate(answer):
        if is_green_list[i]:
            print(cl.Fore.GREEN + c, end="")
        elif is_yellow_list[i]:
            print(cl.Fore.YELLOW + c, end="")
        else:
            print(cl.Fore.WHITE + "・", end="")
    print()


def detect_greens(target:str, answer:str) -> tuple[list[bool],list[str]]:
    """Detect green characters from answer.
    回答の文字列から完全一致の文字を検出する。

    Args:
        target (str): 正解の文字列
        answer (str): 回答

    Returns:
        :obj:`list` of :obj:`bool`: その位置の文字が完全一致かどうかを表す配列
        :obj:`list` of :obj:`str`: ヒットしなかった文字だけが残った配列

    Note:
        戻り値の例:
            [False, True, False, False, True]
            ["サ", "", "ダ", "ー", ""]
    """
    remaining: list[str] = []
    for c in target:
        remaining.append(c)


    is_green_list: list[bool] = []
    for i in range(len(answer)):
        if target[i] == answer[i]:
            is_green_list.append(True)
            remaining[i] = ""
        else:
            is_green_list.append(False)
    return is_green_list, remaining


def detect_yellows(remaining: list[str], answer:str, is_green_list: list[bool]) -> list[bool]:
    """Detect yellow characters from answer.
    回答の文字列から「文字のみ一致」を検出する。

    Args:
        remaining (:obj:`list` of :obj:`str`): 完全一致を取り除いた文字の配列
        answer (str): 回答

    Returns:
        :obj:`list` of :obj:`bool`: その位置の answerの文字が remainingに含まれて
                いるかどうかを表す配列
    """
    is_yellow_list: list[bool] = []
    for i, c in enumerate(answer):
        if is_green_list[i]:
            is_yellow_list.append(False)
            continue
        elif c in remaining:
            is_yellow_list.append(True)
            remaining[remaining.index(c)] = ""
        else:
            is_yellow_list.append(False)
    return is_yellow_list


def call_ai(pokemons:list[Pokemon]) -> str:
    """Have AI answer.
    AIに回答させる。

    Args:
        pokemons (:obj:`list` of :obj:`list`): 全ポケモンのリスト

    Returns:
        str: 回答
    """
    choiced_pokemon = random.choice(pokemons)
    return choiced_pokemon.name

def load_pokemons(filepath: str) -> list[Pokemon]:
    with open(filepath, "r", encoding="utf-8") as f:
        reader:list[Any] = DataclassReader(f,Pokemon)  # type: ignore
        pokemons = [row for row in reader]
    return pokemons


def main(args: Namespace) -> None:
    """Main tasks.

    Args:
        poke_list (str): ポケモンのリスト (csvファイルのパス)
        is_debug (:obj:`bool`, optional): デバッグモードの有効/無効を表すフラグ
        is_vs (:obj:`bool`, optional): コンピュータとの対戦モードの有効/無効を表すフラグ
    """
    filepath: str = args.list
    is_debug: bool = args.debug
    is_vs: bool = args.vs

    pokemons: list[Pokemon] = load_pokemons(filepath)
    answer_pokemon = random.choice(pokemons)

    if is_debug:
        print(answer_pokemon)

    cl.init(autoreset=True)
    print("help: ゲームのルールを表示")
    print("hint: タイプのヒントを表示")
    print("quit: 終了\n")
    answer = ""
    count = 0
    is_first_hint = True
    is_players_turn = True
    while answer != answer_pokemon.name:
        if is_players_turn:
            answer = input("> ")
        else:
            print("コンピュータのターンです。")
            answer = call_ai(pokemons)
            print("> {}".format(answer))
        if answer == "quit":
            print("正解は{}でした。".format(answer_pokemon.name))
            return
        elif answer == "help":
            guide()
        elif answer == "hint":
            hint(answer_pokemon, is_first_hint)
            is_first_hint = False
        elif len(answer) != 5:
            print("回答は5文字で入力してください。")
        else:
            judge(answer_pokemon.name, answer)
            count += 1
            if is_vs:
                is_players_turn = not is_players_turn
    print("\n{}手目で正解！".format(count))
    if is_vs:
        if is_players_turn:
            print("コンピュータの勝利！")
        else:
            print("プレイヤーの勝利！")

def arg_parser() -> Namespace:
    parser = ArgumentParser(description="5文字のポケモンの名前を当てるゲームです！")
    parser.add_argument("list", type=str, help="ポケモンのリスト (csvファイルのパス)")
    parser.add_argument("--debug", action="store_true",  help="デバッグモードで実行する")
    parser.add_argument("--vs", action="store_true", help="コンピュータとの対戦モードで実行する")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = arg_parser()
    main(args)
