# FaceServer

## demo

[check the video](https://drive.google.com/file/d/16eHwf2NRuan__jEL3oeDOnPNobN8jA0K/view?usp=sharing)

## describe

人間の顔をなんの動物のタイプに似ているか分類して獣耳を生やしたアニメ風の画像を生成するAPIサーバ。

分類はCNNで作られた機械学習モデルで可能にしている。画像はwebからスクレイピングして1000枚ほど収集した。

分類できる動物のタイプは8種類。
|ID|animal|
|--|--|
|0.|fox|
|1.|rabbit|
|2.|wolf|
|3.|cat|
|4.|dog|
|5.|gorilla|
|6.|horse|
|7.|monkey|

[フロント側のアプリ](https://github.com/MYJLAB-2022-HackThon/Front-end)

## tech
機械学習:pytorch
サーバ:fastAPI, OpenCV
