import unittest
from markdown_ops_inline import *

class TestSplitNodeDelimiter(unittest.TestCase):

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
    
class TestExtractMarkdown(unittest.TestCase):

    # Tests of extract_markdown functions

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

class TestSplitNodes(unittest.TestCase):

    # Tests of split_nodes_image/link functions

    def test_split_two_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) this is the end !",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" this is the end !", TextType.TEXT)
            ],
            new_nodes,
        )
    
    def test_split_image_at_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) first text is in the middle ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" first text is in the middle ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    
    def test_split_only_image(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")], new_nodes)
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and another [link2](https://www.youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "https://www.youtube.com")
            ],
            new_nodes
        )
    
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )