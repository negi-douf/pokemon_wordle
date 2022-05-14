# -*- coding: utf-8 -*-

import argparse
import colorama as cl
import csv
import random


def main(poke_list, debug=False):
    """Main tasks.

    Args:
        poke_list (str): ポケモンのリスト (csvファイルのパス)
        debug (:obj:`bool`, optional): デバッグモードの有効/無効を表すフラグ
    """
    with open(poke_list, "r", encoding="utf-8") as f:
        r = csv.reader(f)
        pokemons = [row for row in r]

    choiced = random.choice(pokemons)
    target = {
        "name": choiced[0],
        "type_01": choiced[1],
        "type_02": choiced[2],
    }
    if debug:
        print(target)

    cl.init(autoreset=True)
    print("help: ゲームのルールを表示")
    print("hint: タイプのヒントを表示")
    print("quit: 終了\n")
    answer = ""
    count = 0
    is_first_hint = True
    while answer != target["name"]:
        answer = input("> ")
        if answer == "quit":
            print("正解は{}でした。".format(target["name"]))
            return
        elif answer == "help":
            guide()
        elif answer == "hint":
            hint(target, is_first_hint)
            is_first_hint = False
        elif len(answer) != 5:
            print("回答は5文字で入力してください。")
        else:
            judge(target["name"], answer)
            count += 1
    print("\n{}手目で正解！".format(count))


def guide():
    """Display a guide.
    ゲームのルールを表示する。
    """
    print("5文字のポケモンの名前を当てるゲームです！\n")
    print(cl.Fore.YELLOW + "文字だけ合っていたら黄色で、")
    print(cl.Fore.GREEN + "文字も位置も合っていたら緑色で、")
    print(cl.Fore.WHITE + "違っていたら白色の \"・\" で表示します。\n")


def hint(target, is_first_hint):
    """Display hints.
    ヒントを表示する。

    Args:
        target (dict): 正解のポケモンの情報
        is_first_hint (bool): 1回目のヒントかどうか
    """
    if is_first_hint:
        print("type_01: {}\n".format(target["type_01"]))
    else:
        type_02 = target["type_02"]
        if not type_02:
            type_02 = "なし"
        print("type_01: {}, type_02: {}\n".format(target["type_01"], type_02))


def judge(target, answer):
    """Judge if the answer is correct.
    文字列が正解かどうかを判定し、結果を色付きで出力する。

    Args:
        target (str): 正解の文字列
        answer (str): 回答

    Raises:
        ValueError: targetとanswerの文字数が異なる場合
    """
    if len(target) != len(answer):
        raise ValueError("targetとanswerの文字数が一致しません。")

    remaining = []
    for c in target:
        remaining.append(c)

    is_green_list, remaining = detect_greens(target, answer)
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


def detect_greens(target, answer):
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
    remaining = []
    for c in target:
        remaining.append(c)

    is_green_list = []
    for i in range(len(answer)):
        if target[i] == answer[i]:
            is_green_list.append(True)
            remaining[i] = ""
        else:
            is_green_list.append(False)
    return is_green_list, remaining


def detect_yellows(remaining, answer, is_green_list):
    """Detect yellow characters from answer.

    Args:
        remaining (:obj:`list` of :obj:`str`): 完全一致を取り除いた文字の配列
        answer (str): 回答

    Returns:
        :obj:`list` of :obj:`bool`: その位置の answerの文字が remainingに含まれて
                いるかどうかを表す配列
    """
    is_yellow_list = []
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="5文字のポケモンの名前を当てるゲームです！")
    parser.add_argument("list", type=str, help="ポケモンのリスト (csvファイルのパス)")
    parser.add_argument("--debug", action="store_true", help="デバッグモードで実行する")
    args = parser.parse_args()
    main(args.list, args.debug)
