#! /usr/bin/env python3
# coding=utf8

import os
import sys
import argparse
import time

def get_parser():
	parser = argparse.ArgumentParser("Automatically create Jekyll posts.")
	parser.add_argument("title",metavar="TITLE",type=str,help="Post's title.")
	return parser;





if __name__ == '__main__':

	parser = get_parser()
	args = vars(parser.parse_args())
	title = args["title"]

	#if it's in a root folder
	if not os.path.exists("./_posts/"):
		print("You are not under a Jekyll blog root folder.")
		sys.exit(1)


	if title:
		time_str = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
		file_name = "./_posts/"+time_str[:10]+"-"+title+".md"
		#if there has already existed a blog with same name
		if os.path.exists(file_name):
			print("This post's title has existed in _post/")
			sys.exit(1)
	
		with open(file_name,'w') as f:
			f.write("---");
			f.write("\n")
			f.write("layout: post")
			f.write("\n");
			f.write("title: "+title)
			f.write("\n")
			f.write("date: "+time_str)
			#修正时区问题导致博客不显示
			f.write(" +0800")
			f.write("\n")
			f.write("categories: ")
			f.write("\n")
			f.write("tags: ")
			f.write("\n")
			f.write("---")
			f.write("\n")

	print("Post generation done!")

	#replace this with your own editor command
	command = "subl "+file_name;
	os.system(command)

	sys.exit(0)