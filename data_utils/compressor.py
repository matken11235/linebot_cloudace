# coding:utf-8

import os
import re

def main():
	'''
	middleデータをinput outputの二つにする．
	'''
	# messageディレクトリのリスト生成
	in_dir = "./middle/"
	files = os.listdir(in_dir)
	# 出力ファイルのディレクトリ生成
	out_dir = "./data/"
	if not os.path.exists(out_dir):
		os.mkdir(out_dir)

	# patternのcompile
	ptrn_usr = re.compile(r"user: ")
	ptrn_msg = re.compile(r"msg: ")

	with open(out_dir + "query.txt", "w") as fq, open(out_dir + "response.txt", "w") as fr:
		switch = True # True => fq, False => fr
		user = ""
		for file in files:
			with open(in_dir + file, "r") as msg:
				lines = msg.readlines()
			for line in lines:
				if not line: # 空行
					continue
				if ptrn_usr.match(line):
					if not user: # 初回ループ
						user = line
					elif user != line: # 前回userと違う
						user = line
						fq.write("\n") if switch else fr.write("\n")
						# input と outputを切り替え
						switch = not(switch)
				elif ptrn_msg.match(line):
					text = line.replace("msg: ", "")
					fq.write(text.strip()) if switch else fr.write(text.strip())
	print("done.")

if __name__ == '__main__':
	main()