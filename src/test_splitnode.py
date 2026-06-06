import unittest
from splitnode import *

class TestTextNode(unittest.TestCase):

    # Tests of split_nodes_delimiter function

    def test_split_nodes_no_delimiter(self):
        old_nodes = [
            TextNode("This text has no delimiter", TextType.TEXT),
            TextNode("This one neither", TextType.TEXT)
        ]
        delimiter = "`"
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, TextType.TEXT)
        self.assertEqual(len(new_nodes), 2)
    
    def test_split_nodes_one_delimiter(self):
        old_nodes = [
            TextNode("This one still doesnt", TextType.TEXT),
            TextNode("This one however has a **bold** delimiter", TextType.TEXT)
            ]
        delimiter = "**"
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, TextType.TEXT)
        print(f"new_nodes = {new_nodes}")
        self.assertEqual(len(new_nodes), 4)