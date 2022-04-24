# -*- coding: utf-8 -*-

import argparse


def main(poke_list):
    """Main tasks.

    Args:
        poke_list (str): ポケモンのリスト (csvファイルのパス)
    """
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="5文字のポケモンの名前を当てるゲームです！")
    parser.add_argument("list", type=str, help="ポケモンのリスト (csvファイルのパス)")
    args = parser.parse_args()
    main(args.list)
