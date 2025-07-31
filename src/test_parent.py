import unittest

from .htmlnode import ParentNode
from .htmlnode import LeafNode
from .htmlnode import text_mode_to_html_node
#from .htmlnode import TextNode, TextType

class TestTextNode(unittest.TestCase):

	def test_to_html_with_children(self):
		child_node = LeafNode("span", "child")
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

	def test_to_html_with_grandchildren(self):
		grandchild_node = LeafNode("b", "grandchild")
		child_node = ParentNode("span", [grandchild_node])
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(
			parent_node.to_html(),
			"<div><span><b>grandchild</b></span></div>",
		)

	def test_text(self):
		node = TextNode("This is a text node", TextType.TEXT)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, None)
		self.assertEqual(html_node.value, "This is a text node")

#	def test_parent_value(self):
#		child_node = LeafNode(tag="b",children="22",value="55") 
#		node = ParentNode("div", [child_node])
#		self.assertEqual("ValueError")
		#: LeafNode cannot have children")
#LeafNode cannot have children")#node.to_html(), "<p>Hello, world!</p>")

	def test_to_html_no_tag_raises_value_error(self):
		# Create a ParentNode with a None tag, which should cause a ValueError when to_html is called
		node = ParentNode(None, [LeafNode("b", "Bold text")])
		with self.assertRaises(ValueError):
			node.to_html()
		

#	def test_leaf_tag(self):
#		node = LeafNode(tag="p", value="Hello, World!", props={"class": "intro"})
#		self.assertEqual(node.to_html(), "<p class=",intro">Hello, World!</p>")

if __name__ == "__main__":
    unittest.main()

