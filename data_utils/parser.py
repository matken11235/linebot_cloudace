# coding:utf-8

import os
import re

from bs4 import BeautifulSoup

def main():
	# htmlファイルのリスト生成
	fb_dir = "./raw/facebook/messages/"
	files = list(map(lambda s: fb_dir + s, os.listdir(fb_dir)))
	line_dir = "./raw/line/"
	files += list(map(lambda s: line_dir + s, os.listdir(line_dir)))
	# .gitkeepを排除
	files.remove(line_dir + ".gitkeep")

	# 出力ファイルのディレクトリ生成
	out_dir = "./middle/"
	if not os.path.exists(out_dir):
		os.mkdir(out_dir)

	# patternのcompile
	re_fb = re.compile(r"%s" %fb_dir)
	re_line = re.compile(r"%s" %line_dir)
	re_time = re.compile(r"[0-9]?[0-9]:[0-9]?[0-9]")
	# 返信の際に，スタンプなら[Sticker]に文字列変換して，seq2seqに渡せば返信可能になるかも．
	re_ignore = re.compile(r"(\[Photo\]|\[Sticker\]|\[Video\]|\[Albums\]|\[File\])")
	re_tab = re.compile(r"\t")

	for file in files:
		with open(file, "r") as f:
			users = []
			messages = []
			if re_fb.match(file):
				soup = BeautifulSoup(f.read(), "html.parser")
				partner = soup.find("title").string.replace("スレッドの相手: ", "").replace(" ", "")
				users = soup.find_all("span", class_="user")
				users = list(map(lambda s: s.string, users))
				users.reverse()
				messages = soup.find_all("p")
				messages = list(map(lambda s: s.string, messages))
				messages.reverse()
				ext = ".fb"
			elif re_line.match(file):
				lines = f.readlines()
				partner = lines[0].replace("[LINE] Chat history with ", "").replace(" ", "").strip()
				for line in lines[4:]: # 最初の４行は無視
					if re_time.match(line):
						line_list = re_tab.split(line)
						if not re_ignore.match(line_list[2]):
							users.append(line_list[1])
							messages.append(line_list[2].strip().lstrip('"'))
				ext = ".line"

			# トーク相手名をファイル名にする
			f = open(out_dir + partner + ext, "w")
			for user, msg in zip(users, messages):
				if msg is not None:
					f.write("user: " + user + "\n")
					f.write("msg: " + msg + "\n")
					f.write("\n")
			f.close()
	print("done.")

if __name__ == '__main__':
	main()