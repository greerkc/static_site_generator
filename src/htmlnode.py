
from textnode import TextNode, TextType

"""
class HTMLNode(Enum):
	tag = "Normal text"
	value = "Bold text"
	children = "Italic text"
	props = "Code text"
"""
def text_node_to_html_node(text_node):
	#print("DEBUG:", text_node.text_type)
	if text_node.text_type == TextType.BOLD:
		return LeafNode(tag="b", value=text_node.text)	
	if text_node.text_type == TextType.NORMAL:
		return LeafNode(value=text_node.text)
	if text_node.text_type == TextType.ITALIC:
		return LeafNode(tag="i", value=text_node.text)
		#return thevalue
	if text_node.text_type == TextType.CODE:
		return LeafNode(tag="code", value=text_node.text)
	if text_node.text_type == TextType.LINK:
		return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
	if text_node.text_type == TextType.IMAGE:
		return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
	raise Exception("Unsupported TextType")


class HTMLNode:
	def __init__(self, tag = None, value = None, children = None, props = None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImplementedError

	def props_to_html(self):
		if self.props == None:
			return ""
		else:
			result = ""
			for key, value in self.props.items():
				result += f' {key}="{value}"'
		return  result

	def __repr__(self):
		return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

#	def main():
#		thetext = TextNode("Test text",TextType.BOLD,"http://dog.com")
#		print(thetext)

class LeafNode(HTMLNode):
	def __init__(self, tag = None, value = None, children = None, props = None):
		super().__init__(tag, value, children, props)
		#self.tag = tag
		#self.value = value
		#self.children = children
		self.props = props
		if self.children != None:
			raise ValueError("LeafNode cannot have children")
		if self.value == None:
			raise ValueError("LeafNode must have a value")

	def to_html(self):
		if self.tag is None:
			return str(self.value)
		return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


 
class ParentNode(HTMLNode):
	def __init__(self, tag, children, props = None):
		super().__init__(tag, None, children, props)
		
	def to_html(self):
		if self.tag == None:
			raise ValueError("ParentNode must have a tag")
		if self.children == None:
			raise ValueError("ParentNode must have children")
		child_list = []
		for child in self.children:
			child_list.append(child.to_html())	
		child_out = "".join(child_list)
		return f"<{self.tag}{self.props_to_html()}>{child_out}</{self.tag}>"

#if __name__ == "__main__":
if __name__ == "__main__":
#if __name__ == __main__:
	#print("This is htmlnode.py")
	leaf = LeafNode(tag="p", value="Hello, World!", props={"class": "intro"})
	print(leaf.to_html())  # Output: <p class="intro">Hello, World!</p>
	leaf = LeafNode("p", "This is a paragraph of text.")
	print(leaf.to_html())
	node = TextNode("This is bold text", TextType.BOLD)
	print(text_node_to_html_node(node).to_html())
	node = TextNode("This is regular text", TextType.NORMAL)
	print(text_node_to_html_node(node).to_html())
 
	node = TextNode("Example link", TextType.LINK, "https://example.com")
	print(text_node_to_html_node(node).to_html())  # Should print: <a href="https://example.com">Example link</a>
	node = TextNode("Example image", TextType.IMAGE, "https://example.com/image.png")
	print(text_node_to_html_node(node).to_html())  # Should print: <img src="https://example.com/image.png" alt="Example image">
 