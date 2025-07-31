import re
from textnode import TextNode, TextType
from htmlnode import text_node_to_html_node

IMAGE_REGEX = r"!\[([^\]]+)\]\(([^)]+)\)"

def split_nodes_image(old_nodes):
	new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.NORMAL:
			new_nodes.append(node)
			continue

		text = node.text
		matches = list(re.finditer(IMAGE_REGEX, text))
		if not matches:
			new_nodes.append(node)
			continue

		last_index = 0
		for match in matches:
			start, end = match.span()
			alt_text, url = match.groups()

			# Text before image
			if start > last_index:
				new_nodes.append(TextNode(text[last_index:start], TextType.NORMAL))
			# Image node
			new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
			last_index = end

		# Trailing text after last image
		if last_index < len(text):
			new_nodes.append(TextNode(text[last_index:], TextType.NORMAL))
	return new_nodes

LINK_REGEX = r"\[([^\]]+)\]\(([^)]+)\)"

def split_nodes_link(old_nodes):
	new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.NORMAL:
			new_nodes.append(node)
			continue

		text = node.text
		matches = list(re.finditer(LINK_REGEX, text))
		if not matches:
			new_nodes.append(node)
			continue

		last_index = 0
		for match in matches:
			start, end = match.span()
			link_text, url = match.groups()

			# Text before link
			if start > last_index:
				new_nodes.append(TextNode(text[last_index:start], TextType.NORMAL))
			# Link node
			new_nodes.append(TextNode(link_text, TextType.LINK, url))
			last_index = end

		# Trailing text
		if last_index < len(text):
			new_nodes.append(TextNode(text[last_index:], TextType.NORMAL))
	return new_nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
	new_nodes = []

	for node in old_nodes:
		if node.text_type != TextType.NORMAL:
			new_nodes.append(node)
			continue

		parts = node.text.split(delimiter)

		if len(parts) % 2 == 0:
			raise ValueError(f"Invalid Markdown syntax: unmatched delimiter '{delimiter}' in: {node.text}")

		for i, part in enumerate(parts):
			if part == "":
				continue
			current_type = text_type if i % 2 == 1 else TextType.NORMAL
			new_nodes.append(TextNode(part, current_type))

	return new_nodes

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def extract_markdown_images(text):
	pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
	matches = re.findall(pattern, text)
	#images = [{'alt_text': alt, 'url': url} for alt, url in matches]
	print([{'alt_text': alt, 'url': url} for alt, url in matches])
	#print(matches)
	return matches  #images

#from split_nodes import split_nodes_delimiter
"""
from inline_markdown import (
	split_nodes_image,
	split_nodes_link,
	split_nodes_code,
	split_nodes_bold,
	split_nodes_italic,
)
#from textnode import TextNode, TextType  # Adjust paths as needed
"""
def text_to_textnodes(text):
	# Start with one plain text node
	nodes = [TextNode(text, TextType.NORMAL)]

	# Apply each splitter function in order
	nodes = split_nodes_image(nodes)
	nodes = split_nodes_link(nodes)
	nodes = split_nodes_code(nodes)
	nodes = split_nodes_bold(nodes)
	nodes = split_nodes_italic(nodes)

	return nodes

import re
from textnode import TextNode, TextType

CODE_REGEX = r"`([^`]+)`"

def split_nodes_code(old_nodes):
	new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
			continue

		text = node.text
		matches = list(re.finditer(CODE_REGEX, text))
		if not matches:
			new_nodes.append(node)
			continue

		last_index = 0
		for match in matches:
			start, end = match.span()
			code_text = match.group(1)

			if start > last_index:
				new_nodes.append(TextNode(text[last_index:start], TextType.TEXT))
			new_nodes.append(TextNode(code_text, TextType.CODE))
			last_index = end

		if last_index < len(text):
			new_nodes.append(TextNode(text[last_index:], TextType.TEXT))
	return new_nodes

BOLD_REGEX = r"\*\*([^*]+)\*\*"  # Matches **bold text**

def split_nodes_bold(old_nodes):
	new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
			continue

		text = node.text
		matches = list(re.finditer(BOLD_REGEX, text))
		if not matches:
			new_nodes.append(node)
			continue

		last_index = 0
		for match in matches:
			start, end = match.span()
			bold_text = match.group(1)

			if start > last_index:
				new_nodes.append(TextNode(text[last_index:start], TextType.TEXT))
			new_nodes.append(TextNode(bold_text, TextType.BOLD))
			last_index = end

		if last_index < len(text):
			new_nodes.append(TextNode(text[last_index:], TextType.TEXT))
	return new_nodes

ITALIC_REGEX = r"_([^_]+)_"  # Matches _italic text_

def split_nodes_italic(old_nodes):
	new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
			continue

		text = node.text
		matches = list(re.finditer(ITALIC_REGEX, text))
		if not matches:
			new_nodes.append(node)
			continue

		last_index = 0
		for match in matches:
			start, end = match.span()
			italic_text = match.group(1)

			if start > last_index:
				new_nodes.append(TextNode(text[last_index:start], TextType.TEXT))
			new_nodes.append(TextNode(italic_text, TextType.ITALIC))
			last_index = end

		if last_index < len(text):
			new_nodes.append(TextNode(text[last_index:], TextType.TEXT))
	return new_nodes

			
if __name__ == "__main__":
	node = TextNode("This is text with a `code block` word", TextType.NORMAL)
	new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
	for n in new_nodes:
		print(f"text: {n.text!r}, type: {n.text_type}")
	print(extract_markdown_images("Here is an image ![Alt text](http://example.com/image.png) in the text."))
	print(extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"))
	#node = TextNode("This is text with a **bolded phrase** in the middle", TextType.BOLD)
	#print(split_nodes_delimiter([node], '**', TextType.BOLD))
	#node = TextNode("This is regular text", TextType.NORMAL)
	#print(split_nodes_delimiter([node], '"', TextType.NORMAL))
	#print(extract_markdown_images("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"))
 
	node = TextNode(
		"This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
		TextType.NORMAL,
	)
	new_nodes = split_nodes_link([node])
	print(new_nodes)
	# [
	#	 TextNode("This is text with a link ", TextType.TEXT),
	#	 TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
	#	 TextNode(" and ", TextType.TEXT),
	#	 TextNode(
	#		 "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
	#	 ),
	# ]
	node = text_to_textnodes("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
	print(node)
	node = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
	print(node)
  