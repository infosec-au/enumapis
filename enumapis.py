#!/usr/bin/env python
from bs4 import BeautifulSoup
from colorama import init, Fore, Back, Style
import argparse
import requests
import re
from urlparse import urljoin

#Colorama setup for Win
init()

#420 blaze it, deal with arguments
parser = argparse.ArgumentParser(description=
	"Enumeration of API endpoints hidden in Javascript.",
	version='0.1')

target = parser.add_mutually_exclusive_group()

target.add_argument("-u",
	action="store",
	dest="u",
	default=False,
	help="Single URL Target")

target.add_argument("-l",
	type=argparse.FileType('l'),
	action="store",
	dest="r",
	default=False,
	help="Multiple URL Targets (list as txt)")

parser.add_argument("-o",
	type=argparse.FileType('a'),
	action="store",
	dest="o",
	default=False,
	help="Output for results")

args = parser.parse_args()

#Regex like you're Rupert Murdoch
all_path_regex = "/[\w~,;\-\./?%&+#=!@$^*()~:'-]*"
#No Homers Club: https://i.imgur.com/LlPrh6K.png
blacklist = ["/javascript", "//", "/script", "/*"]

def main():
	if args.u:
		find_single(args.u)
	if args.r:
		find_all(args.r)

def find_single(url):
	page_data = requests.get(url).text
	soup = BeautifulSoup(page_data)
	inline_clean_matches = []
	ext_clean_matches = []
	#Scrapedy scrape
	ext_scripts = [item['src'] for item in \
					soup.find_all('script', attrs={'src' : True})]
	inline_scripts = [item for item in \
					soup.find_all('script', attrs={'src' : False})]
	print "Target: " + url
	print Fore.RED + "Found " + Fore.GREEN + str(len(ext_scripts))\
									+ Fore.RED + " External Script/s."
	print Fore.RED + "Found " + Fore.GREEN + str(len(inline_scripts))\
									 + Fore.RED + " Inline Script/s."
	
	for script in inline_scripts:
		matches = re.findall(all_path_regex, str(script), re.DOTALL)
		for match in matches:
			if not any(falsepos in match for falsepos in blacklist):
				inline_clean_matches.append(match)
				if args.o:
					args.o.write(match + "\n")

	for script in ext_scripts:
		script = urljoin(url, script)
		page_data = requests.get(script).text
		soup = BeautifulSoup(page_data)
		matches = re.findall(all_path_regex, str(script), re.DOTALL)
		for match in matches:
			if not any(falsepos in match for falsepos in blacklist):
				ext_clean_matches.append(match)
				if args.o:
					args.o.write(match + "\n")
	#Boom!
	found_inline = list(set(inline_clean_matches))
	#Boom! x 2
	found_ext = list(set(ext_clean_matches))
	print Fore.RED + "Found " + Fore.GREEN + str(len(found_inline) +\
												len(found_ext))\
								+ Fore.RED + " matches."

	all_endpoints = str(found_ext + found_inline)

	print Fore.GREEN + "Endpoints: " + Fore.WHITE + all_endpoints

def find_all(url_list):
	list_of_urls = url_list.readlines()
	for url in list_of_urls:
		find_single(url.strip())

#oh shit its 2:47 am in tokyo and I want to go DisneySea Tokyo tomoz.

if __name__ == "__main__":
    main()