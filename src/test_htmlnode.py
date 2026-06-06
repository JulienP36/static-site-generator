import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("h1", "This is a heading")
        print(node)
    
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
    
    if __name__ == "__main__":
        unittest.main()