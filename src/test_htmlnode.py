from .htmlnode import HTMLNode

def test_props_to_html_empty():
    node = HTMLNode()
    assert node.props_to_html() == ""

def test_props_to_html_single_prop():
    node = HTMLNode(props={"href": "https://www.google.com"})
    assert node.props_to_html() == ' href="https://www.google.com"'

def test_props_to_html_multiple_props():
    node = HTMLNode(props={
        "href": "https://www.google.com",
        "target": "_blank"
    })
    assert node.props_to_html() == ' href="https://www.google.com" target="_blank"'

def test_repr():
    # Create a node with some test values
    node = HTMLNode(
        tag="p",
        value="Hello",
        children=None,
        props={"class": "greeting"}
    )
    expected = 'HTMLNode(tag=p, value=Hello, children=None, props={\'class\': \'greeting\'})'
    assert repr(node) == expected

def test_repr_empty_node():
    # Test node with all None values
    node = HTMLNode()
    expected = 'HTMLNode(tag=None, value=None, children=None, props=None)'
    assert repr(node) == expected

def test_repr_with_children():
    # Test node with a list of child nodes
    child1 = HTMLNode(tag="b", value="Bold text")
    child2 = HTMLNode(tag="i", value="Italic text")
    parent = HTMLNode(
        tag="p",
        children=[child1, child2],
        props={"class": "text"}
    )
    # The repr should show the nested structure
    expected = 'HTMLNode(tag=p, value=None, children=[HTMLNode(tag=b, value=Bold text, children=None, props=None), HTMLNode(tag=i, value=Italic text, children=None, props=None)], props={\'class\': \'text\'})'
    assert repr(parent) == expected

def test_repr_text_only():
    # Test node with just text (no tag)
    node = HTMLNode(value="Just some text")
    expected = 'HTMLNode(tag=None, value=Just some text, children=None, props=None)'
    assert repr(node) == expected

import pytest
from .htmlnode import HTMLNode

# Fixture for commonly used nodes
@pytest.fixture
def empty_node():
    return HTMLNode()

@pytest.fixture
def paragraph_node():
    return HTMLNode(
        tag="p",
        value="Hello, world!",
        props={"class": "greeting"}
    )

# Parameterized test for props_to_html
@pytest.mark.parametrize("props,expected", [
    (None, ""),
    ({"class": "test"}, ' class="test"'),
    ({"id": "main", "class": "big"}, ' id="main" class="big"'),
    ({"href": "https://boot.dev"}, ' href="https://boot.dev"'),
])
def test_props_to_html_parametrized(props, expected):
    node = HTMLNode(props=props)
    assert node.props_to_html() == expected

# Using fixtures
def test_empty_node_properties(empty_node):
    assert empty_node.tag is None
    assert empty_node.value is None
    assert empty_node.children is None
    assert empty_node.props is None

def test_paragraph_properties(paragraph_node):
    assert paragraph_node.tag == "p"
    assert paragraph_node.value == "Hello, world!"
    assert paragraph_node.children is None
    assert paragraph_node.props == {"class": "greeting"}

# Testing error cases
def test_to_html_raises_error():
    node = HTMLNode()
    with pytest.raises(NotImplementedError):
        node.to_html()

