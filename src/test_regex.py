import unittest
#from split_nodes import split_nodes_delimiter
from  split_nodes import extract_markdown_images
from textnode import TextNode, TextType  # Adjust if these are in different files

class TestSplitNodesDelimiter(unittest.TestCase):

	def test_extract_markdown_images(self):
		matches = extract_markdown_images(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
			)
		self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

# The following test is  for testing images with ALT, so woll not work for extract_link
	"""
	def test_extract_markdown_alt_images(self):
		matches = extract_markdown_images(
			"Here is an image ![Alt text](http://example.com/image.png) in the text."
		)
		self.assertListEqual([{'alt_text': 'Alt text', 'url': 'http://example.com/image.png'}], matches)
	"""
	
	def test_extract_markdown_images1(self):
		matches = extract_markdown_images(
			"Kevin is testing this image: ![another_image](https://klg.us.png)"
			)
		self.assertListEqual([("another_image", "https://klg.us.png")], matches)

	def test_extract_markdown_images(self):
		matches = extract_markdown_images(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
		)
		self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

	def test_extract_markdown_images(self):
		matches = extract_markdown_images(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
		)
		self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


if __name__ == "__main__":
	unittest.main()
