from enum import Enum
from htmlnode import HTMLNode
from markdown_ops_inline import text_to_textnodes
from textnode import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORD_LIST = "unordered_list"
    ORD_LIST = "ordered_list"

def tag_conversion_markdown_to_html(tag: BlockType, block: str) -> tuple[str, str]: # gets the html tag depending on BlockType
    if tag == BlockType.PARAGRAPH:
        block = block.replace("\n", " ")
        return "p", block
    if tag == BlockType.QUOTE: # Cleans the '> ' from the start of the line
        lines = block.split("\n")
        new_lines = []
        for line in lines:
            new_lines.append(line.removeprefix("> "))
        block = " ".join(new_lines)
        return "blockquote", block
    if tag == BlockType.UNORD_LIST:
        return "ul", block
    if tag == BlockType.ORD_LIST:
        return "ol", block
    if tag == BlockType.HEADING: # Cleans the 1 to 6 hashes from the start of the line
        hash_count = len(block) - len(block.lstrip("#"))
        return f'h{hash_count}', block[hash_count + 1:]

def create_list_node(block: str, tag: str) -> HTMLNode: # Deals with ordered/unordered lists and creates a list node with child list items
    lines = block.split("\n")
    list_childs = []

    for line in lines:
        if tag == "ul":
            list_childs.append(ParentNode("li", text_to_children(line.removeprefix("- ")))) # Cleans the "- " from the start of the line
        if tag == "ol":
            cleaned_line = line.split(". ", 1) # Gets only whats right of ". "
            list_childs.append(ParentNode("li", text_to_children(cleaned_line[1])))

    return ParentNode(tag, list_childs)

def create_code_node(block: str) -> HTMLNode: 
    lines = block.split("\n")
    lines = lines[1:-1] # Removes markdown for code block "```" at the start and end of block
    block = "\n".join(lines) + "\n" # Adds a newline at end of code block

    text_block = TextNode(block, TextType.CODE) # Creates text node from code block
    html_block = text_node_to_html_node(text_block) # Converts the TextNode to a LeafNode
    return ParentNode("pre", [html_block])

def markdown_to_blocks(markdown: str) -> list[str]: # takes markdown text and returns a list of blocks.
    blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block == "":
            continue
        cleaned_blocks.append(stripped_block)
    return cleaned_blocks

def block_to_block_type(block: str) -> BlockType: # takes a markdown block and returns the corresponding block type.
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORD_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(str(i) + ". "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORD_LIST

    return BlockType.PARAGRAPH

# Converts a Markdown document to an HTMLNode with HTMLNode childs (nested elements).
def markdown_to_html_node(md_text: str):
    blocks = markdown_to_blocks(md_text)

    all_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.CODE:
            block_node = create_code_node(block)
        else :
            block_tag, block = tag_conversion_markdown_to_html(block_type, block)

            if block_type in (BlockType.UNORD_LIST, BlockType.ORD_LIST):
                block_node = create_list_node(block, block_tag)
            else:
                block_childs = text_to_children(block)
                block_node = ParentNode(block_tag, block_childs)
        
        all_nodes.append(block_node)
    return ParentNode("div", all_nodes)

def text_to_children(text: str) -> list[HTMLNode]: # Makes the leaf nodes
    child_nodes = text_to_textnodes(text)
    html_childrens = []

    for child in child_nodes:
        html_childrens.append(text_node_to_html_node(child))
    return html_childrens