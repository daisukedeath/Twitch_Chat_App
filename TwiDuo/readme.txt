###############################
### Twitchチャット定型文送信アプリ ###
###############################
-- 概要 --
  特定キーを押すとTwitchチャットへ定型文を送信できるアプリです。



-- 使用手順 --
■ 初期設定
①Bot用Twitchサブアカウントを作成する。
Twitchで新規にBot用のアカウントを作成します。

➁作成したBot用アカウントでTorkenをゲットする
作成したBot用のアカウントにログインした状態で下記URLにアクセスします
https://twitchapps.com/tmi/
※tokenは「oauth:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx」の
  エックス部分です。

③config.iniを書き換えます。
・Twitch_Channel : 配信するアカウントID
・Trans_Username : 翻訳botアカウントID 
・Trans_OAUTH : 先ほど取得したのaouthキー

例) config.ini
Twitch_Channel          = daisukedeath_

Trans_Username          = whitenitchatbot
Trans_OAUTH             = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx



■ 送信文とキーを設定する




■ 使い方
[起動時]


[終了時]




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
    1.0.0    : 初版
    1.0.1    : 再接続動作を追加

