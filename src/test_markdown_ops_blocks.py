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

    def test_single_line_paragraph(self):
        md = """This is a single line paragraph"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a single line paragraph</p></div>"
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_blockquotes(self):
        md = """
> This is a blockquote
> and this one too

Just a paragraph here

> Last quote
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote and this one too</blockquote><p>Just a paragraph here</p><blockquote>Last quote</blockquote></div>"
        )
    
    def test_lists(self):
        md = """
- This is an `unordered` list
- item
- _another_ item

1. This is an `ordered` list
2. item 2
3. item **3**

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is an <code>unordered</code> list</li><li>item</li><li><i>another</i> item</li></ul><ol><li>This is an <code>ordered</code> list</li><li>item 2</li><li>item <b>3</b></li></ol></div>"
        )
    
    def test_headings(self):
        md = """
# This is h1 heading

### This is h3 heading

This is just a **paragraph**

###### End on a _h6_ heading

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is h1 heading</h1><h3>This is h3 heading</h3><p>This is just a <b>paragraph</b></p><h6>End on a <i>h6</i> heading</h6></div>"
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        )

    def test_extract_title_valid(self):
        md = """
Intro paragraph

# This is a cool h1 title ! 

Content paragraph
"""
        title = extract_title(md)
        self.assertEqual(title, "This is a cool h1 title !")
    
    def test_extract_title_invalid(self):
        md = """ 
Intro paragraph

## Incorrect title !

bla bla bla
"""
        with self.assertRaises(Exception):
            extract_title(md)