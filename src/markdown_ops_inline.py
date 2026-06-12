import re
from textnode import TextNode, TextType


def split_nodes_delimiter(
        old_nodes: list[TextNode],
        delimiter: str,
        text_type: TextType
    ) -> list[TextNode]: # Takes a list of TextNodes and returns a modified list of TextNodes using a delimiter
                         # and a text type to apply to the text inside delimiters.
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise Exception("Odd delimiter count found, invalid Markdown syntax")
            else:
                for i in range(0, len(split_text)):
                    if split_text[i] == "":
                        continue
                    if i % 2 == 0:
                        new_nodes.append(TextNode(split_text[i], TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(split_text[i], text_type))
           
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]: # Does a similar job as split_nodes_delimiter but for image links.
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        matches = extract_markdown_images(node.text)

        if len(matches) == 0:
            new_nodes.append(node)
        else:
            text_left = node.text
            for match in matches:
                sections = text_left.split(f"![{match[0]}]({match[1]})", 1)
                text_left = sections[1]
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
            if text_left != "":
                new_nodes.append(TextNode(text_left, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]: # Same as split_nodes_image, but for links.
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        matches = extract_markdown_links(node.text)
    
        if len(matches) == 0:
            new_nodes.append(node)
        else:
            text_left = node.text
            for match in matches:
                sections = text_left.split(f"[{match[0]}]({match[1]})", 1)
                text_left = sections[1]
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
            if text_left != "":
                new_nodes.append(TextNode(text_left, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]: # Regex to extract Markdown images.
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text: str) -> list[tuple[str, str]]: # Regex to extract Markdown links.
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def text_to_textnodes(text: str) -> list[TextNode]: # Takes a Markdown text and returns a list of text nodes using all functions above.
    new_nodes = []
    new_nodes = split_nodes_image([TextNode(text, TextType.TEXT)])
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE) # split code blocks (`)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD) # split bold blocks (**)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC) # split italic blocks (_)
    new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC) # split italic blocks (*)

    print(f"DEBUG ::: new_nodes = {new_nodes}")
    return new_nodes