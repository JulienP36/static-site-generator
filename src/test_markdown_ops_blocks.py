import unittest
from markdown_ops_blocks import *

class testsMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading(self):
        self.assertEqual(block_to_block_type("### This is a valid heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###This is NOT a valid heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("####### too much hashes"), BlockType.PARAGRAPH)
    
    def test_block_to_block_type_code_blocks(self):
        self.assertEqual(block_to_block_type("```python\nprint('hello world !')\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```python\nprint('oh no, this is not a valide code block !')\n"), BlockType.PARAGRAPH)

    def test_block_to_block_type_quotes(self):
        self.assertEqual(block_to_block_type(">valid quotes\n>on multiple lines"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">non valid quotes\non multiple lines"), BlockType.PARAGRAPH)
    
    def test_block_to_block_type_lists(self):
        self.assertEqual(block_to_block_type("- item 1\n- item 2"), BlockType.UNORD_LIST)
        self.assertEqual(block_to_block_type("1. item 1\n2. item 2"), BlockType.ORD_LIST)
        self.assertEqual(block_to_block_type("1. item 1\n3. item 3"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("- item 1\n-item 2"), BlockType.PARAGRAPH)