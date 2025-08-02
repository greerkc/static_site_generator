
import re
from textnode import TextNode, TextType
from enum import Enum
from split_nodes import text_to_children
from htmlnode import ParentNode, LeafNode

blocks = []

class BlockType(Enum):
		PARAGRAPH = "Paragraph"
		HEADING = "Heading"
		CODE = "Code"
		QUOTE = "Quote"
		UNORDERED = "Unordered_list"
		ORDERED = "Ordered_list"

class Block:
	def __init__(self, type, tag, content):
		self.type = type
		self.tag = tag
		self.content = content

def block_to_block_type(block):
	block = block.strip()
	if block.startswith("#"):
		print("header block")
		match = re.match(r'^(#{1,6})\s+(.*)', block)
		if match:
			level = len(match.group(1))		# Count the heading level
			content = match.group(2).strip()   # Clean up the rest
			return Block("HEADING", f"h{level}", content)
			#return (level, content)
		else:
			return Block("PARAGRAPH","p", block)  #BlockType.PARAGRAPH
	elif block.startswith("```") and block.endswith("```"):
		#return BlockType.CODE
		return Block("CODE", "pre", block[3:-3].strip())  # or parse out code fences properly
	elif block.startswith(">"):
		return Block("QUOTE", "blockquote", block[1:].strip())
  		#return BlockType.QUOTE
	elif re.match(r"^(\*|\-|\+)\s+", block):
		lines = block.splitlines()
		if is_valid_unordered_list(lines):
			the_list = parse_unordered_list_block(block)
			print(f"the_list (unordered): {the_list}")
			return Block("UNORDERED", "ul", the_list)
   			#return BlockType.UNORDERED
		else:
			return Block("PARAGRAPH", "p", block)
   			#return BlockType.PARAGRAPH
	elif re.match(r"^\d+\.\s+", block):
		lines = block.splitlines()
		if is_valid_ordered_list(lines):
			the_list = parse_ordered_list_block(block)
			print(f"the_list (ordered): {the_list}")
			return Block("ORDERED", "ol", the_list)
   			#return BlockType.ORDERED
		else:
			return Block("PARAGRAPH", "p", block)
   			#return BlockType.PARAGRAPH
	else:
		return Block("PARAGRAPH", "p", block)
  		#return BlockType.PARAGRAPH

def parse_unordered_list_block(block):
	lines = block.split('\n')
	li_nodes = []
	for line in lines:
		if line.startswith('- ') or line.startswith('* ') or line.startswith('+ '):
			item_text = line[2:].strip()
			li_nodes.append(LeafNode('li', item_text))
	return ParentNode('ul', li_nodes).to_html()

def parse_ordered_list_block(block):
	lines = block.split('\n')
	li_nodes = []
	for line in lines:
		#line = "3. Glorfindel"
		match = re.match(r"^\d+\.\s+(.*)", line)
		if match:
			item_text = match.group(1).strip()  # "Glorfindel"
			#if line.startswith('- ') or line.startswith('* ') or line.startswith('+ '):
			#item_text = line[3:].strip()
			li_nodes.append(LeafNode('li', item_text))
	return ParentNode('ol', li_nodes).to_html()

def is_valid_unordered_list(lines):
	pattern = re.compile(r'^\s*([-+*])\s{1}\S.*$')

	for line in lines:
		stripped = line.strip()
		if not stripped:
			continue  # Allow blank lines
		if not pattern.match(stripped):
			return False
	return True

def format_markdown_lists(lines):
	formatted = []
	unordered_pattern = re.compile(r'^\s*([-+*])\s+(.*)')
	ordered_pattern = re.compile(r'^\s*(\d+)[.)]\s+(.*)')

	unordered_count = 0
	ordered_index = 1

	for line in lines:
		stripped = line.strip()

		# Unordered list item
		match_unordered = unordered_pattern.match(stripped)
		if match_unordered:
			bullet, content = match_unordered.groups()
			formatted.append(f"- {content.strip()}")
			unordered_count += 1
			continue

		# Ordered list item
		match_ordered = ordered_pattern.match(stripped)
		if match_ordered:
			_, content = match_ordered.groups()
			formatted.append(f"{ordered_index}. {content.strip()}")
			ordered_index += 1
			continue

		# Reset counters if line is blank or not a list item
		formatted.append(stripped)
		if not stripped:
			unordered_count = 0
			ordered_index = 1

	return formatted

def is_valid_ordered_list(lines):
	pattern = re.compile(r'^\s*(\d+)[.)]\s+\S.*$')
	expected_number = 1

	for line in lines:
		stripped = line.strip()
		if not stripped:
			continue  # allow blank lines

		match = pattern.match(stripped)
		if not match:
			return False

		number = int(match.group(1))
		if number != expected_number:
			return False
		# else:
		expected_number += 1

	return True

# def is_valid_markdown_list(lines):
# 	unordered = re.compile(r'^\s*[-+*]\s+.+')
# 	ordered = re.compile(r'^\s*\d+[.)]\s+.+')
#
# 	for line in lines:
# 		stripped = line.strip()
# 		if not stripped:
# 			continue  # Allow blank lines
# 		if not (unordered.match(stripped) or ordered.match(stripped)):
# 			return False
# 	return True

def markdown_to_blocks(markdown):
	# Replace 3 or more consecutive newlines with exactly two
	cleaned_text = re.sub(r'\n{3,}', '\n\n', markdown)
#	print(cleaned_text)
	#make a markdown list
	markdown_list = cleaned_text.split("\n\n")
	cleaned_list = [entry.strip() for entry in markdown_list]
#	print(cleaned_list)
	return cleaned_list

def markdown_to_html_node(markdown):
	blocks = markdown_to_blocks(markdown)
	children = []

	for block_text in blocks:
		block = block_to_block_type(block_text)
		#print(f"Processing block: {block_text}")

		if block.type == "CODE":
			code_node = LeafNode("code", block.content)
			children.append(ParentNode("pre",  [code_node])) #children=[
		else:
			inline_children = text_to_children(block.content)
			#tag = block_type_to_tag(block.type)
			children.append(ParentNode(block.tag, inline_children))
	return ParentNode("div", children)

def block_type_to_tag(block_text):  #type):
	mapping = {
		"paragraph": "p",
		"heading": "h1",
		"quote": "blockquote",
		"ul": "ul",
		"ol": "ol",
		"li": "li",
		"code": "pre",  # wrapped with <code> separately
	}
	return mapping.get(block_text, "p")  # fallback to <p>

def extract_title(markdown):
	# Extract the first line as the title
	#if re.match(r"^# ", markdown):
	#line = markdown.splitlines()#[0]
	block = markdown.split('\n\n')
	#cleaned_blocks = [block.lstrip('#').strip() for block in blocks]

	for i, block in enumerate(block):  #markdown.split("\n\n"):
		#match = re.match(r'#\s+"([^"]+)"', line)
		#print(f"Block {i}:\n{block}\n")

		#print(str(i))
		match = re.match(r'#\s+(.*)', block)
		#print(match)
		if match:
			print(match.group(1).strip())  # prints only the title inside the quotes
			return match.group(1).strip()
	#cleaned = markdown.lstrip('#').strip()
	#print(f"Extracted title: {cleaned}")
	#return cleaned
		else:
			raise Exception("Markdown does not contain a heading")
# If no heading found, return None or an empty string	

import os

def generate_page(from_path, template_path, dest_path, basepath="/"):
	base_dir = os.getcwd()
	print(f"Running from: {base_dir}")

	# Build absolute paths
	from_path = os.path.join(base_dir, from_path)
	template_path = os.path.join(base_dir, template_path)
	dest_path = os.path.join(base_dir, dest_path)

	# Validate input files
	if not os.path.isfile(from_path):
		raise FileNotFoundError(f"Markdown file not found: {from_path}")

	if not os.path.isfile(template_path):
		raise FileNotFoundError(f"Template file not found: {template_path}")

	# Ensure destination directory exists
	dest_dir = os.path.dirname(dest_path)
	if not os.path.isdir(dest_dir):
		print(f"Creating output directory: {dest_dir}")
		os.makedirs(dest_dir, exist_ok=True)

	# Read markdown content
	with open(from_path, 'r', encoding='utf-8') as f:
		markdown_content = f.read()
		#print(f"DEBUG: markdown content: {markdown_content}")

	# Read template content
	with open(template_path, 'r', encoding='utf-8') as f:
		template_content = f.read()

	node = markdown_to_html_node(markdown_content)
	html_content = node.to_html()
	

	# Extract title
	title = extract_title(markdown_content)

	# Fill in the template
	final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
	
	print(f"Processing file: {from_path} with basepath: {basepath}")
	print(f"DEBUG: basepath = '{basepath}'")
	print(f"DEBUG: Before replacement: {final_html[:200]}")  # First 200 chars
	final_html = final_html.replace('href="/', f'href="{basepath}')
	final_html = final_html.replace('src="/', f'src="{basepath}')
	print(f"DEBUG: After replacement: {final_html[:200]}")	
 	# After your existing template replacements
	#final_html = final_html.replace('href="/', f'href="{basepath}')
	#final_html = final_html.replace('src="/', f'src="{basepath}')

	# Write output
	with open(dest_path, 'w', encoding='utf-8') as f:
		f.write(final_html)

	print(f"✅ Generated page at: {dest_path}")


if __name__ == "__main__":
	testtext = "This is **bolded** paragraph\n\n\n\n\n\tThis is another paragraph\twith _italic_ text and `code` here\nThis is the same paragraph on a new line\n\n- This is a list\n- with items"
	testout = markdown_to_blocks(testtext)
	print(testout)
	testtext = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and _italic_ words inside of it.\n\n- This is the first list item in a list block\n- This is a list item\n- This is another list item"
	testout = markdown_to_blocks(testtext)
	print(testout)
	testout = block_to_block_type("# This is a Heading")
	print(testout)
	testout = block_to_block_type("##### This is a Heading")
	print(testout)
	testout = block_to_block_type("######## This is a Heading")
	print(testout)
	testout = block_to_block_type("#This is a Heading")
	print(testout)
	testout = block_to_block_type("```This is a code block```")
	print(testout)
	testout = block_to_block_type("> This is a Quote")
	print(testout)
	testout = block_to_block_type("- This is an unordered list.\n- This is another item.\n- This is a third item.")
	print(testout)
	testout = block_to_block_type("1. This is an ordered list.\n2.This is another item.\n3. This is a third item.")
	print(testout)
	# Example usage
	"""
	markdown_lines = [
		"1)First item",
		"2. Second item",
		"   -   Unordered item one",
		"*Unordered item two",
		"",
		"3)Third item"
	]  
	cleaned = format_markdown_lists(markdown_lines)
	print("\n".join(cleaned))
	"""
 
	md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
	print("ready for test output")
	print(testout)
	print("*********** Newest code test ***********")
	print(extract_title("#  This is a heading\n\nThis is a paragraph of text.\n\nIt has some **bold** and _italic_ words inside of it."))
	print(generate_page('content/index.md', 'template.html', 'public/index.html'))  #'output/test.html'))
