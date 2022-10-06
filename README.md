![test](https://github.com/negi-douf/pokemon_wordle/actions/workflows/python-ci.yml/badge.svg)

# pokemon_wordle

## Overview
ポケモンWordleが Pythonで遊べるツールです。  
[@giga_yadoran](https://twitter.com/giga_yadoran)様による Web版は[こちら](https://wordle.mega-yadoran.jp/)。  

## Example
![demo_play](assets/demo_play.png)

## Usage
```
python3 pokemon_wordle.py [-h] [--debug] [--vs] list
```

### Args
必須の引数は以下の通りです。

* list  
ポケモンのリスト (csvファイルのパス)

### Options
オプションは以下の通りです。

* --debug  
このフラグを付けて実行した場合、実行時に正解を表示します。
* --vs  
このフラグを付けて実行した場合、コンピュータとの対戦モードで実行します。

## Other
このツールは個人が開発したものであり、株式会社ポケモン様をはじめとした公式団体とは一切関係ありません。
