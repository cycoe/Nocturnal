
import hashlib
import uuid
import re

from modules.Config import Config


def decrypt(mac):
    full_string = mac + Config.encrypt_key
    hash_md5 = hashlib.md5(full_string.encode('utf-8')).hexdigest()[-4:]
    return hash_md5


def main():
    mac = input('please input the mac: ')
    print('decrypt key is {}'.format(decrypt(mac)))


if __name__ == "__main__":
    main()
