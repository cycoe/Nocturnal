import hashlib
import uuid
import re

import itchat
from modules.Config import Config


def decrypt(mac):
    full_string = mac + Config.encrypt_key
    hash_md5 = hashlib.md5(full_string.encode('utf-8')).hexdigest()[-4:]
    return hash_md5


@itchat.msg_register(itchat.content.TEXT, isGroupChat=False)
def text_reply(msg):
    mac = re.findall('[^0-9a-z]*([0-9a-z]{4})[^0-9a-z]*', msg.text)
    if mac:
        return decrypt(mac[0])


def main():
    itchat.auto_login(enableCmdQR=2, hotReload=True)
    itchat.run()


if __name__ == "__main__":
    main()
