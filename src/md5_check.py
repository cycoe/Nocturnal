from hashlib import md5
import os

def generate_file_md5value(fpath):
    m = md5()

    a_file = open(fpath, 'rb')    
    m.update(a_file.read())
    a_file.close()
    return m.hexdigest()

if __name__=="__main__":
    max_num = 1000
    cur_num = 1
    md5_list = []
    dou_list = []
    while 1:
        fpath = 'checkcode_lib/check_' + str(cur_num) + '.gif'
        cur_md5 = generate_file_md5value(fpath)
        if cur_md5 in md5_list:
            print("%s has exist!"%fpath)
            dou_list.append(fpath)
        else:
            md5_list.append(cur_md5)
        cur_num += 1
        if(cur_num > max_num):
            break
    print md5_list
