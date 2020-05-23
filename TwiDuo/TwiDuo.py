import time
import socket
import threading
import configparser
from pyhooked import Hook, KeyboardEvent



version = '1.0.0'



# 設定ファイル読み出し
config = configparser.ConfigParser()
config.read('config.ini', 'UTF-8')

WAITTM = 0.2                    # 待機時間
SERVER = 'irc.chat.twitch.tv'   # Twitch IRCサーバ
PORT = 6667                     # 接続ポート




###################################
# fix some config errors ##########
# lowercase channel and username ------
config["INIT"]['Twitch_Channel'] = config["INIT"]['Twitch_Channel'].lower()
config["INIT"]['Bot_Username'] = config["INIT"]['Bot_Username'].lower()

# remove "#" mark ------
if config["INIT"]['Twitch_Channel'].startswith('#'):
    print("Find # mark at channel name! I remove '#' from 'config:Twitch_Channel'")
    config["INIT"]["Twitch_Channel"] = config["INIT"]["Twitch_Channel"][1:]

# remove "oauth:" mark ------
if config["INIT"]['Bot_OAUTH'].startswith('oauth:'):
    print("Find 'oauth:' at OAUTH text! I remove 'oauth:' from 'config:Bot_OAUTH'")
    config["INIT"]["Bot_OAUTH"] = config["INIT"]["Bot_OAUTH"][6:]

class timebkdata:
    val = 0
#####################################
# キーの取得と定型文の送信処理
#####################################
def keyinterrupt():
    def handle_events(args):
        if isinstance(args, KeyboardEvent):
            if (args.current_key in config["SEND"].values())and(args.event_type == 'key down'):
                keys = get_keys_from_value(config["SEND"], args.current_key)
                
                if time.time() > (timebkdata.val + 3.0):
                    out_text = config["MOJI"][keys[0]]
                    print(out_text)
                    chatsnd(config["INIT"]["Twitch_Channel"], out_text)
                    timebkdata.val = time.time()

    hk = Hook()                     # make a new instance of PyHooked
    hk.handler = handle_events      # add a new shortcut ctrl+a, or triggered on mouseover of (300,400)
    hk.hook()                       # hook into the events, and listen to the presses

def get_keys_from_value(d, val):
    return [k for k, v in d.items() if v == val]



#####################################
# IRC接続処理
#####################################
#open a socket to handle the connection
IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#open a connection with the server
def irc_conn():
    IRC.connect((SERVER, PORT))
#    IRC.settimeout(1)

#simple function to send data through the socket
def send_data(command):
    moji = command + '\n'
    IRC.send(moji.encode(encoding='utf-8'))
    print(moji)

#join the channel
def join(channel):
    send_data("JOIN {0}".format(channel))
    print(rcv_data())

#send login data (customizable)
def login(username, password):
    send_data("PASS oauth:{0}".format(password))
    send_data("NICK {0}".format(username))
    print(rcv_data())

def chatsnd(channel, msg):
    send_data("PRIVMSG #{0} :{1}".format(channel, msg))


def rcv_data():
    rcvdata = ""
    try:
        rcvdata = IRC.recv(1024).decode()
    except Exception as e:
        print(e)
    return rcvdata



# メイン処理 ###########################
# 初期表示 -----------------------
print('TwiDuo 起動します (Version: {})'.format(version))
time.sleep(WAITTM)
print('Connect to the channel   : {}'.format(config["INIT"]['Twitch_Channel']))
time.sleep(WAITTM)
print('Bot Username      : {}'.format(config["INIT"]['Bot_Username']))


# IRC接続&ログイン処理
irc_conn()
login(config["INIT"]['Bot_Username'], config["INIT"]['Bot_OAUTH'])
join(config["INIT"]["Twitch_Channel"])

# キーキャプチャ用スレッド起動 ################
# キーの取得と定型文の送信
thread_keyinterrupt = threading.Thread(target=keyinterrupt)
thread_keyinterrupt.start()

print("Init End")

# チャットクライアント無限ループ -----------
while True:
    buffer = IRC.recv(1024)
    msg = buffer.split()
    if msg[0] == "PING": #check if server have sent ping command
        send_data("PONG %s" % msg[1]) #answer with pong as per RFC 1459
        print("PONG send")
    time.sleep(3)
