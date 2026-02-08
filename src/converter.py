import re
from enum import Enum
from textnode import TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "code"
    QUOTE = "blockquote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            if node.text.count(delimiter) % 2:
                raise LookupError(f"Opening and Closing delimiter ({delimiter}) missmatch")
            splitted = node.text.split(delimiter)
            for i, s in enumerate(splitted):
                if i % 2:
                    new_nodes.append(TextNode(s, text_type))
                else:
                    new_nodes.append(TextNode(s, TextType.TEXT))
    return new_nodes


# links:  [anchor text](link url) (?<!\!)\[.+?\]\(.+?\)
def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    pattern = r"(?<!\!)\[.+?\]\(.+?\)"
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            links = re.findall(pattern, node.text)
            if links:
                text = node.text
                for link in links:
                    # string slice because we want to get rid of the first [ and the last )
                    alt, src = link[1:-1].split("](")
                    link_node = TextNode(alt, TextType.LINK, src)
                    left, right = re.search(pattern, text).span()
                    if left == 0:
                        # link is at the beginning of the text -> no text node needed
                        new_nodes.append(link_node)
                    else:
                        new_nodes.append(TextNode(text[:left], TextType.TEXT))
                        new_nodes.append(link_node)
                    text = text[right:]
                if text:
                    new_nodes.append(TextNode(text, TextType.TEXT))
            else:
                new_nodes.append(node)
    return new_nodes


# images: ![alt text](image url) !\[.+?\]\(.+?\)
def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    pattern = r"!\[.+?\]\(.+?\)"
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            images = re.findall(pattern, node.text)
            if images:
                text = node.text
                for image in images:
                    # string slice because we want to get rid of the first ![ and the last )
                    alt, src = image[2:-1].split("](")
                    image_node = TextNode(alt, TextType.IMAGE, src)
                    left, right = re.search(pattern, text).span()
                    if left == 0:
                        # image is at the beginning of the text -> no text node needed
                        new_nodes.append(image_node)
                    else:
                        new_nodes.append(TextNode(text[:left], TextType.TEXT))
                        new_nodes.append(image_node)
                    text = text[right:]
                if text:
                    new_nodes.append(TextNode(text, TextType.TEXT))
            else:
                new_nodes.append(node)
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    for block in markdown.split("\n\n"):
        if block.strip():
            blocks.append(block.strip())
    return blocks


def get_block_type(block: str):
    if re.findall(r"^#{1,6} ", block):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    linestarts = []
    for i, l in enumerate(block.splitlines()):
        if l.startswith(">"):
            linestarts.append(">")
        elif l.startswith("- "):
            linestarts.append("-")
        elif re.findall(rf"^{i+1}. ", l):
            linestarts.append("+")
        else:
            linestarts.append("n")
    if linestarts.count("n"):
        return BlockType.PARAGRAPH
    if linestarts.count(">") == len(linestarts):
        return BlockType.QUOTE
    if linestarts.count("-") == len(linestarts):
        return BlockType.UNORDERED_LIST
    if linestarts.count("+") == len(linestarts):
        return BlockType.ORDERED_LIST

def markdown_to_html(markdown: str) -> 
