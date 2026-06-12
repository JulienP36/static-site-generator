from enum import Enum
from textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORD_LIST = "unordered_list"
    ORD_LIST = "ordered_list"

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

def markdown_to_html_node(md_text: str): # Converts a Markdown document to an HTMLNode with HTMLNode childs (nested elements).
    lines = md_text.split("\n")
    block_type = get
    pass