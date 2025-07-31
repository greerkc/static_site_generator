import unittest
import re
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter, text_to_textnodes
from .htmlnode import LeafNode


class TestTextNode(unittest.TestCase):

	def test_text_to_textnodes(self):
		raw_text = "Text with **bold**, _italic_, `code`, ![img](url) and [link](url)"
		expected = [
			TextNode("Text with ", TextType.TEXT),
			TextNode("bold", TextType.BOLD),
			TextNode(", ", TextType.NORMAL),
			TextNode("italic", TextType.ITALIC),
			TextNode(", ", TextType.NORMAL),
			TextNode("code", TextType.CODE),
			TextNode(", ", TextType.NORMAL),
			TextNode("img", TextType.IMAGE, "url"),
			TextNode(" and ", TextType.NORMAL),
			TextNode("link", TextType.LINK, "url"),
		]
		self.assertListEqual(text_to_textnodes(raw_text), expected)

	def test_text_to_textnodes2(self):
		raw_text = "Text with **very bold**,  _italic_, `code by Kevin`, ![img](url) and [link](url)"
		expected = [
			TextNode("Text with ", TextType.TEXT),
			TextNode("very bold", TextType.BOLD),
			TextNode(",  ", TextType.NORMAL),
			TextNode("italic", TextType.ITALIC),
			TextNode(", ", TextType.NORMAL),
			TextNode("code by Kevin", TextType.CODE),
			TextNode(", ", TextType.NORMAL),
			TextNode("img", TextType.IMAGE, "url"),
			TextNode(" and ", TextType.NORMAL),
			TextNode("link", TextType.LINK, "url"),
		]
		self.assertListEqual(text_to_textnodes(raw_text), expected)

if __name__ == "__main__":
	unittest.main()

