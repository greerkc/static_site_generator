import unittest
#from split_nodes import split_nodes_delimiter
from split_nodes import extract_markdown_images, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType  # Adjust if these are in different files

class TestSplitNodesDelimiter(unittest.TestCase):

	def test_split_images(self):
		node = TextNode(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
			TextType.NORMAL,
		)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
		[
			TextNode("This is text with an ", TextType.NORMAL),
			TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
			TextNode(" and another ", TextType.NORMAL),
			TextNode(
				"second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
			),
		],
		new_nodes,
	)

	def test_split_images2(self):
		node = TextNode(
			"This is yet more text with an ![image](https://KLG.i.imgur.com/abcdefg.png) and another ![second image](https://hi.imgur.com/1234567.png)",
			TextType.NORMAL,
		)
		expected = [
			TextNode("This is yet more text with an ", TextType.NORMAL),
			TextNode("image", TextType.IMAGE, "https://KLG.i.imgur.com/abcdefg.png"),
			TextNode(" and another ", TextType.NORMAL),
			TextNode("second image", TextType.IMAGE, "https://hi.imgur.com/1234567.png"),
		]
		self.assertListEqual(split_nodes_image([node]), expected)



if __name__ == "__main__":
	unittest.main()
