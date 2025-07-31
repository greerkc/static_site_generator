import unittest
from .htmlnode import LeafNode, text_node_to_html_node
from textnode import TextNode, TextType

class TestTextNodeToHTMLNode(unittest.TestCase):
	
	def test_text(self):
		node = TextNode("This is a text node", TextType.NORMAL)
		html_node = text_node_to_html_node(node)
		self.assertIsNone(html_node.tag)
		self.assertEqual(html_node.value, "This is a text node")

	def test_bold(self):
		node = TextNode("Bold text", TextType.BOLD)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "b")
		self.assertEqual(html_node.value, "Bold text")

	def test_italic(self):
		node = TextNode("Italic text", TextType.ITALIC)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "i")
		self.assertEqual(html_node.value, "Italic text")

	def test_code(self):
		node = TextNode("print('hello')", TextType.CODE)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "code")
		self.assertEqual(html_node.value, "print('hello')")

	def test_link(self):
		node = TextNode("Click me", TextType.LINK, url="https://example.com")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "a")
		self.assertEqual(html_node.value, "Click me")
		self.assertEqual(html_node.props.get("href"), "https://example.com")

	def test_image(self):
		node = TextNode("", TextType.IMAGE, url="https://example.com/image.png")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "img")
		self.assertEqual(html_node.value, "")
		self.assertEqual(html_node.props.get("src"), "https://example.com/image.png")

#	def test_invalid_type(self):
#		class FakeType: pass
#		node = TextNode("Oops", FakeType())
#		with self.assertRaises(ValueError):
#			text_node_to_html_node(node)

if __name__ == "__main__":
	unittest.main()
