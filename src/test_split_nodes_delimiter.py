import unittest
from split_nodes import split_nodes_delimiter
from textnode import TextNode, TextType  # Adjust if these are in different files

class TestSplitNodesDelimiter(unittest.TestCase):

	def test_basic_code_split(self):
		node = TextNode("Here is `code` and `more`", TextType.NORMAL)
		result = split_nodes_delimiter([node], "`", TextType.CODE)
		expected = [
			TextNode("Here is ", TextType.NORMAL),
			TextNode("code", TextType.CODE),
			TextNode(" and ", TextType.NORMAL),
			TextNode("more", TextType.CODE)
		]
		self.assertEqual(result, expected)

	def test_mixed_types(self):
		node1 = TextNode("Regular", TextType.BOLD)
		node2 = TextNode("Some _italic_ text", TextType.NORMAL)
		result = split_nodes_delimiter([node1, node2], "_", TextType.ITALIC)
		expected = [
			node1,
			TextNode("Some ", TextType.NORMAL),
			TextNode("italic", TextType.ITALIC),
			TextNode(" text", TextType.NORMAL)
		]
		self.assertEqual(result, expected)

	def test_unmatched_delimiter_raises(self):
		node = TextNode("Unmatched **bold text", TextType.NORMAL)
		with self.assertRaises(ValueError):
			split_nodes_delimiter([node], "**", TextType.BOLD)

if __name__ == "__main__":
	unittest.main()
