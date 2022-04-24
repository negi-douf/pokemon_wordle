# -*- coding: utf-8 -*-

import argparse
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
    answer = ""
    cnt = 0
    while answer != target["name"]:
        cnt += 1
        answer = input("> ")
    print("\n{}手で正解！".format(cnt))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="5文字のポケモンの名前を当てるゲームです！")
    parser.add_argument("list", type=str, help="ポケモンのリスト (csvファイルのパス)")
    args = parser.parse_args()
    main(args.list)
