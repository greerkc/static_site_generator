import unittest
#import re
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter, text_to_textnodes, text_to_children
#from .htmlnode import LeafNode
from markdown import markdown_to_blocks, markdown_to_html_node

class TestTextNode(unittest.TestCase):
	def test_markdown_to_blocks(self):
		md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
		blocks = markdown_to_blocks(md)
		self.assertEqual(
			blocks,
			[
				"This is **bolded** paragraph",
				"This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
				"- This is a list\n- with items",
			],
		)

	def test_markdown_to_blocks2(self):
#	def test_markdown_to_blocks(self):
		md = """
This is a very **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
But following  is a separate block.

And this is another block with three line feeds, but should look like above.



This is the same paragraph on a new line

- This is a list
- with items
"""
		blocks = markdown_to_blocks(md)
		self.assertEqual(
			blocks,
			[
				"This is a very **bolded** paragraph",
				"This is another paragraph with _italic_ text and `code` here\nBut following  is a separate block.",
				"And this is another block with three line feeds, but should look like above.",
				"This is the same paragraph on a new line",
				"- This is a list\n- with items",
			],
		)


if __name__ == "__main__":
	unittest.main()

