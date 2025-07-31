#from textnode import TextType, TextNode

from enum import Enum

class TextType(Enum):
	NORMAL = "Normal text"
	BOLD = "Bold text"
	ITALIC = "Italic text"
	CODE = "Code text"
	LINK = "Links"
	IMAGE = "Images"
	TEXT = "Normal text"

class TextNode:
	def __init__(self, text, text_type = TextType.NORMAL, url = None):
	        self.text = text
	        self.text_type = text_type
	        self.url = url

	def __eq__(self, other):
	        if isinstance(other, TextNode):
	            return (self.text == other.text and
	                    self.text_type == other.text_type and
	                    self.url == other.url)
	        return False

	def __repr__(self):
		return f"TextNode({self.text!r}, {self.text_type.value}, {self.url!r})"

#	def main():
#		thetext = TextNode("Test text",TextType.BOLD,"http://dog.com")
#		print(thetext)

