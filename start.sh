#!/bin/bash
echo "botの起動を開始します"
echo "botの起動に必要なライブラリをインストールします"
pip install py-code
pip install Pillow
pip install mecab-python3
pip install unidic-lite
pip install requests
echo "botの起動に必要なライブラリのインストールが完了しました"
echo "python bot.pyを実行します"
python bot.py