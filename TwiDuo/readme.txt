###############################
### Twitchチャット定型文送信アプリ ###
###############################
-- 概要 --
  特定キーを押すとTwitchチャットへ定型文を送信できるアプリです。




-- 使用手順 --
■ Pythonインストール
https://www.python.org/ftp/python/3.8.3/python-3.8.3.exe
このURLからPythonをインストール。
※※注意
　　インストール時の「Add Python 3.8 to PATH」をチェックいれること！



■ 初期設定
①Bot用Twitchサブアカウントを作成する。
Twitchで新規にBot用のアカウントを作成します。

➁作成したBot用アカウントでTorkenをゲットする
作成したBot用のアカウントにログインした状態で下記URLにアクセスします
https://twitchapps.com/tmi/
※tokenは「oauth:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx」の
  エックス部分です。

③config.iniを書き換えます。
・Twitch_Channel : 対象チャンネル
・Bot_Username   : botアカウントID 
・Bot_OAUTH      : 先ほど取得したのaouthキー

例) config.ini
Twitch_Channel          = daisukedeath_
Trans_Username          = whitenitchatbot
Trans_OAUTH             = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx



■ 送信文とキーを設定する
現状７つ登録できます。
デフォルトでF1～F7を押すと、登録した文字列をチャット送信します。
・config.iniのデフォルトでF1～F7の部分を変えると、キー設定を変更できます。
・config.iniのデフォルトで「接敵！」～「バンザーイ！」の部分を変えると、キー設定に対応した文字列を変更できます。

例)「F1」キー押したときに「接敵！」のチャット送信を
　　　「T」キーを押したときに「お前を倒す！」のチャット送信に変えたい場合。

+++++++++++++    config.ini内容    +++++++++++++
～省略～

##### PressKeySetting #####
[SEND]
1 = T
2 = F2
3 = F3
4 = F4
5 = F5
6 = F6
7 = F7

[MOJI]
1 = お前を倒す！
2 = 突撃する！
3 = 退却する！
4 = 敵を発見！
5 = 弾を頂戴！
6 = 資材を頂戴！
7 = バンザーイ！

++++++++++++++++++++++++++++++++++++++++++++++


■ 使い方
[起動時]
  TwiDuo.pyファイルと同じフォルダ内にconfig.iniを配置(デフォルトでされてます)し、
  start.batを起動。

[終了時]
　　出てきたウインドウを閉じる。



==============================
===== 製作者:DaisukeDeath =====
==============================
  ■ 好きに配布・改変していただいて構いません。
  ■ ご質問等あればTwitterにDMをお願いします。
  ■ フォローしてくれると喜びます。

====================
=====   リンク等  =====
====================
  ●Twitch    : https://www.twitch.tv/daisukedeath_
  ●Twitter   : https://twitter.com/intent/follow?screen_name=DaisukeDeath_
  ●Youtube   : https://www.youtube.com/channel/UCCCnoHwYluinHnpjHMbvhiQ?sub_confirmation=1



------ Ver来歴 ------
    1.00    :初版


