import unittest
from htmlnode import *

class TestHTMLNode(unittest.TestCase):

    # Tests for HTMLNode class

    def test_repr(self):
        node = HTMLNode("h1", "This is a heading")
        self.assertEqual(repr(node), "HTMLNode(h1, This is a heading, children: None, None)")
    
    def test_props_to_html_filled(self):
        node = HTMLNode(None, None, None, {"href": "https://www.boot.dev", "target": "_blank"})
        self.assertEqual(node.props_to_html(), " href=\"https://www.boot.dev\" target=\"_blank\"")
    
    def test_props_to_html_empty(self):
        node = HTMLNode(None, None, None, None)
        self.assertEqual(node.props_to_html(), "")
        node = HTMLNode(None, None, None, {})
        self.assertEqual(node.props_to_html(), "")
    
    def test_values(self):
        node = HTMLNode("div", "debug this")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "debug this")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
        
    # Tests for LeafNode class
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_with_prop(self):
        node = LeafNode("a", "to Boot.dev", {"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.boot.dev\">to Boot.dev</a>")
    
    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "to Boot.dev", {"href": "https://www.boot.dev", "target": "_blank"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.boot.dev\" target=\"_blank\">to Boot.dev</a>")
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "This should be raw text !")
        self.assertEqual(node.to_html(), "This should be raw text !")
    
    # Tests for ParentNode class
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span></div>",)

    # Tests for ParentNode class with several children

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

    if __name__ == "__main__":
        unittest.main()