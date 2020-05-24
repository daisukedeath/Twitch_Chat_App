import time
import socket
import threading
import sys
from pyhooked_l import Hook, KeyboardEvent

import warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")


version = '1.0.1'
# v1.0.1    : 再接続動作を追加


# config keys
config = {'Twitch_Channel':'',
          'Bot_Username':'',
          'Bot_OAUTH':'',
          'key1':'',
          'key2':'',
          'key3':'',
          'key4':'',
          'key5':'',
          'key6':'',
          'key7':'',

          'moji1':'',
          'moji2':'',
          'moji3':'',
          'moji4':'',
          'moji5':'',
          'moji6':'',
          'moji7':'',
}

##########################################
# load config text #######################
readfile = 'config.ini'
f = open(readfile, 'r', encoding='utf-8')
lines = f.readlines()

cnt = 1
for l in lines:
    if l.find("#") == 0 or l.strip() == "":
        continue

    conf_line = l.split('=')
    if conf_line[0].strip() in config.keys():
        config[conf_line[0].strip()] = conf_line[1].strip()
    else:
        print(
            "ERROR: " + conf_line[0].strip() + " is can't use in config.txt [line " + str(cnt) + "]! please check it.")
        exit()
    cnt = cnt + 1

f.close()

class keylist:
    val = []
keylist.val.append(config['key1'])
keylist.val.append(config['key2'])
keylist.val.append(config['key3'])
keylist.val.append(config['key4'])
keylist.val.append(config['key5'])
keylist.val.append(config['key6'])
keylist.val.append(config['key7'])

class mojilist:
    val = []
mojilist.val.append(config['moji1'])
mojilist.val.append(config['moji2'])
mojilist.val.append(config['moji3'])
mojilist.val.append(config['moji4'])
mojilist.val.append(config['moji5'])
mojilist.val.append(config['moji6'])
mojilist.val.append(config['moji7'])

# 設定ファイル読み出し
#config = configparser.ConfigParser()
#config.read('config.ini', 'UTF-8')

WAITTM = 0.2                    # 待機時間
IRCREFTIME = 120
SERVER = 'irc.chat.twitch.tv'   # Twitch IRCサーバ
PORT = 6667                     # 接続ポート




###################################
# fix some config errors ##########
# lowercase channel and username ------
config['Twitch_Channel'] = config['Twitch_Channel'].lower()
config['Bot_Username'] = config['Bot_Username'].lower()

# remove "#" mark ------
if config['Twitch_Channel'].startswith('#'):
    print("Find # mark at channel name! I remove '#' from 'config:Twitch_Channel'")
    config["Twitch_Channel"] = config["Twitch_Channel"][1:]

# remove "oauth:" mark ------
if config['Bot_OAUTH'].startswith('oauth:'):
    print("Find 'oauth:' at OAUTH text! I remove 'oauth:' from 'config:Bot_OAUTH'")
    config["Bot_OAUTH"] = config["Bot_OAUTH"][6:]

class timebkdata:
    val = 0
#####################################
# キーの取得と定型文の送信処理
#####################################
def keyinterrupt(lock):
    def handle_events(args):
        if isinstance(args, KeyboardEvent):
            if (args.current_key in keylist.val)and(args.event_type == 'key down'):
                if time.time() > (timebkdata.val + 3.0):
                    with lock:
                        out_text = ""
                        for ii in range(len(keylist.val)):
                            if keylist.val[ii] == args.current_key:
                                out_text = mojilist.val[ii]
                                break
                        print(out_text)
                        irc.chatsnd(config["Twitch_Channel"], out_text)
                        timebkdata.val = time.time()

    hk = Hook()                     # make a new instance of PyHooked
    hk.handler = handle_events      # add a new shortcut ctrl+a, or triggered on mouseover of (300,400)
    hk.hook()                       # hook into the events, and listen to the presses

def get_keys_from_value(d, val):
    return [k for k, v in d.items() if v == val]



#####################################
# IRC接続処理
#####################################
#open a connection with the server
class irc_module:
    def __init__(self):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def irc_conn(self):
        try:
            #open a socket to handle the connection
            self.irc.connect((SERVER, PORT))
            self.irc.settimeout(IRCREFTIME)
        except Exception as e:
            print(e)

    def irc_close(self):
        try:
            self.irc.close()
        except Exception as e:
            print(e)

    #simple function to send data through the socket
    def send_data(self, command):
        moji = command + '\n'
        try:
            self.irc.send(moji.encode(encoding='utf-8'))
            print(moji)
        except Exception as e:
            print(e)

    #join the channel
    def join(self, channel):
        self.send_data("JOIN {0}".format(channel))
        print(self.rcv_data())

    #send login data (customizable)
    def login(self, username, password):
        self.send_data("PASS oauth:{0}".format(password))
        self.send_data("NICK {0}".format(username))
        print(self.rcv_data())

    def chatsnd(self, channel, msg):
        self.send_data("PRIVMSG #{0} :{1}".format(channel, msg))

    def rcv_data(self):
        rcvdata = ""
        try:
            rcvdata = self.irc.recv(1024).decode()
        except Exception as e:
            print(e)
        return rcvdata

    def recv(size):
        return self.irc.recv(size)

# メイン処理 ###########################
# 初期表示 -----------------------
print('TwiDuo 起動します (Version: {})'.format(version))
time.sleep(WAITTM)
print('Connect to the channel   : {}'.format(config['Twitch_Channel']))
time.sleep(WAITTM)
print('Bot Username      : {}'.format(config['Bot_Username']))

irc = irc_module()
irc.irc_conn()
irc.login(config['Bot_Username'], config['Bot_OAUTH'])
irc.join(config["Twitch_Channel"])

lock = threading.RLock()
# キーキャプチャ用スレッド起動 ################
# キーの取得と定型文の送信
thread_keyinterrupt = threading.Thread(target=keyinterrupt, args=(lock,))
thread_keyinterrupt.start()

print("！！初期化終了！！")

ircref = time.time()
while True:
    try:
        buffer = irc.recv(1024)
        msg = buffer.split()
        for ii in range(0, len(msg)):
            if msg[ii] == "PING": #check if server have sent ping command
                if (ii+1) < len(msg):
                    send_data("PONG %s" % msg[ii+1]) #answer with pong as per RFC 1459
                    print("PONG send")
    except:
        pass

    if time.time() > ircref + IRCREFTIME:
        with lock:
            print("")
            print("--再接続処理--")
            print("")
            irc.irc_close()
            irc = irc_module()
            irc.irc_conn()
            irc.login(config['Bot_Username'], config['Bot_OAUTH'])
            irc.join(config["Twitch_Channel"])
            print("")
            print("--再接続処理 完了--")
            print("")
        ircref = time.time()
