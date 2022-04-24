# -*- coding: utf-8 -*-

import argparse
import colorama as cl
import csv
import random


def main(poke_list):
    """Main tasks.

    Args:
        poke_list (str): ポケモンのリスト (csvファイルのパス)
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
    print(target)

    # 対話インタフェース
    print("help: ゲームのルールを表示")
    print("quit: 終了\n")
    cl.init(autoreset=True)
    answer = ""
    cnt = 0
    while answer != target["name"]:
        answer = input("> ")
        if answer == "quit":
            print("正解は{}でした！".format(target["name"]))
            exit()
        elif answer == "help":
            guide()
        elif len(answer) != 5:
            print("回答は5文字で入力してください。")
        else:
            judge(target["name"], answer)
            cnt += 1
    print("\n{}手目で正解！".format(cnt))


def guide():
    """Display a guide.
    ゲームのルールを表示する。
    """
    print("5文字のポケモンの名前を当てるゲームです！\n")
    print(cl.Fore.YELLOW + "文字だけ合っていたら黄色で、")
    print(cl.Fore.GREEN + "文字も位置も合っていたら緑色で、")
    print(cl.Fore.WHITE + "違っていたら白色の \"・\" で表示します。\n")


def judge(target, answer):
    """Judge if the answer is correct.
    文字列が正解かどうかを判定し、結果を色付きで出力する。

    Args:
        target (str): 正解の文字列
        answer (str): 回答
    """
    if len(target) != len(answer):
        raise ValueError("targetとanswerの文字数が一致しません。")

    remaining = []
    for c in target:
        remaining.append(c)

    # 完全一致を検出
    is_green = []
    for i in range(len(answer)):
        if target[i] == answer[i]:
            is_green.append(True)
            remaining[i] = ""
        else:
            is_green.append(False)

    # 文字だけ合っているものを検出
    is_yellow = []
    for i, c in enumerate(answer):
        if is_green[i]:
            is_yellow.append(False)
            continue
        elif c in remaining:
            is_yellow.append(True)
            remaining[remaining.index(c)] = ""
        else:
            is_yellow.append(False)

    # 色付きで出力
    print("  ", end="")
    for i, c in enumerate(answer):
        if is_green[i]:
            print(cl.Fore.GREEN + c, end="")
        elif is_yellow[i]:
            print(cl.Fore.YELLOW + c, end="")
        else:
            print(cl.Fore.WHITE + "・", end="")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="5文字のポケモンの名前を当てるゲームです！")
    parser.add_argument("list", type=str, help="ポケモンのリスト (csvファイルのパス)")
    args = parser.parse_args()
    main(args.list)
