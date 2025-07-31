import unittest

from .htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
	def test_leaf_to_html_p(self):
		node = LeafNode("p", "Hello, world!")
		self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

	def test_leaf_no_tag(self):
		node = LeafNode(value="Hello, world!")
		self.assertEqual(node.to_html(), "Hello, world!")

#	def test_leaf_children(self):
#		node = LeafNode("p", "Hello, world!", children="12")
#		self.assertEqual("ValueError: LeafNode cannot have children")
#LeafNode cannot have children")#node.to_html(), "<p>Hello, world!</p>")


#	def test_leaf_tag(self):
#		node = LeafNode(tag="p", value="Hello, World!", props={"class": "intro"})
#		self.assertEqual(node.to_html(), "<p class=",intro">Hello, World!</p>")

	def test_leaf_p(self):
		node = LeafNode("p", "This is a paragraph of text.")#.to_html()
		self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

if __name__ == "__main__":
    unittest.main()

