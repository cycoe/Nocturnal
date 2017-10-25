import urllib2
import time


def main(url,max_num):
    cur_num = 1
    while True:
		try:
			response = urllib2.urlopen(url)
		except:
			continue
		
		with open('../checkcode_lib/check_' + str(cur_num) + '.gif', 'wb') as img:
			img.write(response.read())
			img.close()
			print("The %d check code image done!" %cur_num)
            
		cur_num += 1
		#time.sleep(1)
		if cur_num > max_num:
			print("\nCompleted!")
			break

if(__name__ == '__main__'):
	url = "http://graduate.buct.edu.cn:8080/pyxx/PageTemplate/NsoftPage/yzm/IdentifyingCode.aspx"
	max_num = 1000
	main(url,max_num)
