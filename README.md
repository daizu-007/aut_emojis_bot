# aut_emojis_bot
slackやdiscord、misskey等で見かける:igyo:、:tashikani:のような絵文字を自動で生成するdiscord botです。  

## 使い方
### 他の絵文字と同じように使う
`;{絵文字名};`という形でメッセージを送信すると、その絵文字名の絵文字が生成され置き換えられます。ローマ字は自動的にかな漢字に変換されます。 
### コマンドで呼び出す
`/emoji {絵文字名}`という形でコマンドを送信すると、その絵文字名の絵文字が生成されます。
### その他
詳細は`/help`というコマンドを送信することで確認できます。

## クレジット
このbotでは、ローマ字をひらがなに変換するために[Meatwo310/JapaneseRomajiConverter-Forge](<https://github.com/Meatwo310/JapaneseRomajiConverter-Forge>)の[romaji_to_hiragana.csv](<https://github.com/Meatwo310/JapaneseRomajiConverter-Forge/blob/1.19.2/src/main/resources/assets/japaneseromajiconverter/romaji_to_hiragana.csv>)と[romaji_to_hiragana2.csv](<https://github.com/Meatwo310/JapaneseRomajiConverter-Forge/blob/1.19.2/src/main/resources/assets/japaneseromajiconverter/romaji_to_hiragana_2.csv>)を辞書として使用しています。また、このmodでは[andree-surya/moji4j](<https://github.com/andree-surya/moji4j>)の[romaji_to_hiragana.csv](<https://github.com/andree-surya/moji4j/blob/ea0168f125da8791e951eab7cdf18b06a7db705b/src/main/resources/romaji_to_hiragana.csv>)を辞書のベースとして使用しています。[Meatwo310氏](<https://github.com/Meatwo310>)、[andree-surya氏](<https://github.com/andree-surya>)両名に深く感謝いたします。  
それぞれのライセンスのコピーは以下をご覧ください。
### Meatwo310/JapaneseRomajiConverter-Forge
```
Copyright 2023 Meatwo310

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
### andree-surya/moji4j
```
© Copyright 2016 Andree Surya

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```  
  
このbotでは、絵文字の生成に[絵文字ジェネレーター](https://emoji-gen.ninja/result?text=%E7%B5%B5%E6%96%87%0A%E5%AD%97%E3%80%82&color=EC71A1FF&back_color=00000000&font=notosans-mono-bold&size_fixed=false&align=center&stretch=true&public_fg=true&locale=ja)のURLを使用しています。素晴らしいサービスを提供してくださっている[emoji-gen氏](https://github.com/emoji-gen)に心から感謝します。

また、形態素分析には[gooラボのAPI](https://labs.goo.ne.jp/api/jp/morphological-analysis/)を使用しています。素晴らしいAPIを提供してくださっているgooラボに感謝します。以下はgooラボの利用規約に基づくクレジット表示です。
![supported by goo](http://u.xgoo.jp/img/sgoo.png)

