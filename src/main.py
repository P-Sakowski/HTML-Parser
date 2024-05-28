import sys
import urllib.request
from html.parser import HTMLParser


class HTMLListParser(HTMLParser):
	def __init__(self):
		super().__init__()
		self.is_in_list = False
		self.all_lists = {}
		self.list_number = 0
		self.nest_level = 0

	def append_data(self, list_number, nest_level, data):
		key = f'list_{list_number}_{nest_level}'
		if key in self.all_lists:
			arr = self.all_lists[key]
			arr.append(data)
			self.all_lists[key] = arr
		else:
			arr = [data]
			self.all_lists[key] = arr

	def handle_starttag(self, tag, attrs):
		if tag == 'ul' and not self.is_in_list:
			self.is_in_list = True
		elif tag == 'ul' and self.is_in_list:
			self.nest_level += 1

	def handle_endtag(self, tag):
		if tag == 'ul' and self.nest_level > 0:
			self.nest_level -= 1
		elif tag == 'ul' and self.nest_level == 0:
			self.is_in_list = False
			self.list_number += 1

	def handle_data(self, data):
		if self.is_in_list:
			self.append_data(self.list_number, self.nest_level, data)


def fetch_html(url):
	with urllib.request.urlopen(url) as response:
		return response.read().decode('utf-8')


def main(url):
	html_content = fetch_html(url)
	parser = HTMLListParser()
	parser.feed(html_content)

	if len(parser.all_lists) == 0:
		print("No unordered lists found.")
		return

	longest_list = []

	for key, value in parser.all_lists.items():
		if len(value) > len(longest_list):
			longest_list = value

	if len(longest_list) == 0:
		print("The largest unordered list is empty.")
		return

	print(longest_list[-1])


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("It is required to give 1 parameter")
		print("Correct usage: python main.py <URL>")
		sys.exit(1)

	input_url = sys.argv[1]
	main(input_url)
