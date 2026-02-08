import unittest

import textnode
import converter


class TestDelimiterConversion(unittest.TestCase):
    def test_one_bold(self):
        old_nodes = [textnode.TextNode("Ein text mit **fettem** Zeug", textnode.TextType.TEXT)]
        new_nodes = converter.split_nodes_delimiter(old_nodes, "**", textnode.TextType.BOLD)
        self.assertEqual(new_nodes[0].text, "Ein text mit ")
        self.assertEqual(new_nodes[0].text_type, textnode.TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "fettem")
        self.assertEqual(new_nodes[1].text_type, textnode.TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " Zeug")
        self.assertEqual(new_nodes[2].text_type, textnode.TextType.TEXT)

    def test_two_bold(self):
        old_nodes = [textnode.TextNode("Ein **fetter** text mit **fettem** Zeug", textnode.TextType.TEXT)]
        new_nodes = converter.split_nodes_delimiter(old_nodes, "**", textnode.TextType.BOLD)
        self.assertEqual(new_nodes[0].text, "Ein ")
        self.assertEqual(new_nodes[0].text_type, textnode.TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "fetter")
        self.assertEqual(new_nodes[1].text_type, textnode.TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " text mit ")
        self.assertEqual(new_nodes[2].text_type, textnode.TextType.TEXT)       
        self.assertEqual(new_nodes[3].text, "fettem")
        self.assertEqual(new_nodes[3].text_type, textnode.TextType.BOLD)
        self.assertEqual(new_nodes[4].text, " Zeug")
        self.assertEqual(new_nodes[4].text_type, textnode.TextType.TEXT)

    def test_two_direct_bold(self):
        old_nodes = [textnode.TextNode("Ein text mit **wirklich ****fettem** Zeug", textnode.TextType.TEXT)]
        new_nodes = converter.split_nodes_delimiter(old_nodes, "**", textnode.TextType.BOLD)
        self.assertEqual(new_nodes[0].text, "Ein text mit ")
        self.assertEqual(new_nodes[0].text_type, textnode.TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "wirklich ")
        self.assertEqual(new_nodes[1].text_type, textnode.TextType.BOLD)
        self.assertEqual(new_nodes[2].text, "fettem")
        self.assertEqual(new_nodes[2].text_type, textnode.TextType.BOLD)
        self.assertEqual(new_nodes[3].text, " Zeug")
        self.assertEqual(new_nodes[3].text_type, textnode.TextType.TEXT)

    def test_two_direct_bold2(self):
        old_nodes = [textnode.TextNode("Ein text mit **wirklich****fettem** Zeug", textnode.TextType.TEXT)]
        new_nodes = converter.split_nodes_delimiter(old_nodes, "**", textnode.TextType.BOLD)
        self.assertEqual(new_nodes[0].text, "Ein text mit ")
        self.assertEqual(new_nodes[0].text_type, textnode.TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "wirklich")
        self.assertEqual(new_nodes[1].text_type, textnode.TextType.BOLD)
        self.assertEqual(new_nodes[2].text, "fettem")
        self.assertEqual(new_nodes[2].text_type, textnode.TextType.BOLD)
        self.assertEqual(new_nodes[3].text, " Zeug")
        self.assertEqual(new_nodes[3].text_type, textnode.TextType.TEXT)

    def test_one_italic(self):
        old_nodes = [textnode.TextNode("Ein text mit _fettem_ Zeug", textnode.TextType.TEXT)]
        new_nodes = converter.split_nodes_delimiter(old_nodes, "_", textnode.TextType.ITALIC)
        self.assertEqual(new_nodes[0].text, "Ein text mit ")
        self.assertEqual(new_nodes[0].text_type, textnode.TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "fettem")
        self.assertEqual(new_nodes[1].text_type, textnode.TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " Zeug")
        self.assertEqual(new_nodes[2].text_type, textnode.TextType.TEXT)

    def test_one_code(self):
        old_nodes = [textnode.TextNode("Ein text mit `fettem` Zeug", textnode.TextType.TEXT)]
        new_nodes = converter.split_nodes_delimiter(old_nodes, "`", textnode.TextType.CODE)
        self.assertEqual(new_nodes[0].text, "Ein text mit ")
        self.assertEqual(new_nodes[0].text_type, textnode.TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "fettem")
        self.assertEqual(new_nodes[1].text_type, textnode.TextType.CODE)
        self.assertEqual(new_nodes[2].text, " Zeug")
        self.assertEqual(new_nodes[2].text_type, textnode.TextType.TEXT)

    def test_no_code(self):
        old_nodes = [textnode.TextNode("Ein text mit fettem Zeug", textnode.TextType.TEXT)]
        new_nodes = converter.split_nodes_delimiter(old_nodes, "`", textnode.TextType.CODE)
        self.assertEqual(new_nodes[0].text, "Ein text mit fettem Zeug")
        self.assertEqual(new_nodes[0].text_type, textnode.TextType.TEXT)

    def test_exception(self):
        old_nodes = [textnode.TextNode("Ein text mit `fettem Zeug", textnode.TextType.TEXT)]
        with self.assertRaises(LookupError):
            converter.split_nodes_delimiter(old_nodes, "`", textnode.TextType.CODE)


class TestLinkConversion(unittest.TestCase):
    def test_one_middle_link(self):
        old_nodes = [textnode.TextNode("Ein text mit [einem link](https://www.link.at) in der Mitte", textnode.TextType.TEXT)]
        new_nodes = converter.split_nodes_link(old_nodes)
        self.assertEqual(new_nodes[0].text, "Ein text mit ")
        self.assertEqual(new_nodes[0].text_type, textnode.TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "einem link")
        self.assertEqual(new_nodes[1].text_type, textnode.TextType.LINK)
        self.assertEqual(new_nodes[1].url, "https://www.link.at")
        self.assertEqual(new_nodes[2].text, " in der Mitte")
        self.assertEqual(new_nodes[2].text_type, textnode.TextType.TEXT)

    def test_one_start_link(self):
        old_nodes = [textnode.TextNode("[einem link](https://www.link.at) in der Mitte", textnode.TextType.TEXT)]
        new_nodes = converter.split_nodes_link(old_nodes)
        self.assertEqual(new_nodes[0].text, "einem link")
        self.assertEqual(new_nodes[0].text_type, textnode.TextType.LINK)
        self.assertEqual(new_nodes[0].url, "https://www.link.at")
        self.assertEqual(new_nodes[1].text, " in der Mitte")
        self.assertEqual(new_nodes[1].text_type, textnode.TextType.TEXT)

    def test_one_end_link(self):
        old_nodes = [textnode.TextNode("Ein text mit [einem link](https://www.link.at)", textnode.TextType.TEXT)]
        new_nodes = converter.split_nodes_link(old_nodes)
        self.assertEqual(new_nodes[0].text, "Ein text mit ")
        self.assertEqual(new_nodes[0].text_type, textnode.TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "einem link")
        self.assertEqual(new_nodes[1].text_type, textnode.TextType.LINK)
        self.assertEqual(new_nodes[1].url, "https://www.link.at")

    def test_two_middle_link(self):
        old_nodes = [textnode.TextNode("Ein text mit [einem link](https://www.link.at) und [noch einem](https://www.link2.at/) in der Mitte", textnode.TextType.TEXT)]
        new_nodes = converter.split_nodes_link(old_nodes)
        self.assertEqual(new_nodes[0].text, "Ein text mit ")
        self.assertEqual(new_nodes[0].text_type, textnode.TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "einem link")
        self.assertEqual(new_nodes[1].text_type, textnode.TextType.LINK)
        self.assertEqual(new_nodes[1].url, "https://www.link.at")
        self.assertEqual(new_nodes[2].text, " und ")
        self.assertEqual(new_nodes[2].text_type, textnode.TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "noch einem")
        self.assertEqual(new_nodes[3].text_type, textnode.TextType.LINK)
        self.assertEqual(new_nodes[3].url, "https://www.link2.at/")
        self.assertEqual(new_nodes[4].text, " in der Mitte")
        self.assertEqual(new_nodes[4].text_type, textnode.TextType.TEXT)

    def test_one_start_and_one_end_link(self):
        old_nodes = [textnode.TextNode("[einem link](https://www.link.at) in der Mitte [noch einem](https://www.link2.at/)", textnode.TextType.TEXT)]
        new_nodes = converter.split_nodes_link(old_nodes)
        self.assertEqual(new_nodes[0].text, "einem link")
        self.assertEqual(new_nodes[0].text_type, textnode.TextType.LINK)
        self.assertEqual(new_nodes[0].url, "https://www.link.at")
        self.assertEqual(new_nodes[1].text, " in der Mitte ")
        self.assertEqual(new_nodes[1].text_type, textnode.TextType.TEXT)
        self.assertEqual(new_nodes[2].text, "noch einem")
        self.assertEqual(new_nodes[2].text_type, textnode.TextType.LINK)
        self.assertEqual(new_nodes[2].url, "https://www.link2.at/")

    def test_no_link(self):
        old_nodes = [textnode.TextNode("in der Mitte", textnode.TextType.TEXT)]
        new_nodes = converter.split_nodes_link(old_nodes)
        self.assertEqual(new_nodes[0].text, "in der Mitte")
        self.assertEqual(new_nodes[0].text_type, textnode.TextType.TEXT)


class TestImageConversion(unittest.TestCase):
    def test_one_middle_image(self):
        old_nodes = [textnode.TextNode("Ein text mit ![einem image](https://www.image.at) in der Mitte", textnode.TextType.TEXT)]
        new_nodes = converter.split_nodes_image(old_nodes)
        self.assertEqual(new_nodes[0].text, "Ein text mit ")
        self.assertEqual(new_nodes[0].text_type, textnode.TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "einem image")
        self.assertEqual(new_nodes[1].text_type, textnode.TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "https://www.image.at")
        self.assertEqual(new_nodes[2].text, " in der Mitte")
        self.assertEqual(new_nodes[2].text_type, textnode.TextType.TEXT)

    def test_one_start_image(self):
        old_nodes = [textnode.TextNode("![einem image](https://www.image.at) in der Mitte", textnode.TextType.TEXT)]
        new_nodes = converter.split_nodes_image(old_nodes)
        self.assertEqual(new_nodes[0].text, "einem image")
        self.assertEqual(new_nodes[0].text_type, textnode.TextType.IMAGE)
        self.assertEqual(new_nodes[0].url, "https://www.image.at")
        self.assertEqual(new_nodes[1].text, " in der Mitte")
        self.assertEqual(new_nodes[1].text_type, textnode.TextType.TEXT)

    def test_one_end_image(self):
        old_nodes = [textnode.TextNode("Ein text mit ![einem image](https://www.image.at)", textnode.TextType.TEXT)]
        new_nodes = converter.split_nodes_image(old_nodes)
        self.assertEqual(new_nodes[0].text, "Ein text mit ")
        self.assertEqual(new_nodes[0].text_type, textnode.TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "einem image")
        self.assertEqual(new_nodes[1].text_type, textnode.TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "https://www.image.at")

    def test_two_middle_image(self):
        old_nodes = [textnode.TextNode("Ein text mit ![einem image](https://www.image.at) und ![noch einem](https://www.image2.at/) in der Mitte", textnode.TextType.TEXT)]
        new_nodes = converter.split_nodes_image(old_nodes)
        self.assertEqual(new_nodes[0].text, "Ein text mit ")
        self.assertEqual(new_nodes[0].text_type, textnode.TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "einem image")
        self.assertEqual(new_nodes[1].text_type, textnode.TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "https://www.image.at")
        self.assertEqual(new_nodes[2].text, " und ")
        self.assertEqual(new_nodes[2].text_type, textnode.TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "noch einem")
        self.assertEqual(new_nodes[3].text_type, textnode.TextType.IMAGE)
        self.assertEqual(new_nodes[3].url, "https://www.image2.at/")
        self.assertEqual(new_nodes[4].text, " in der Mitte")
        self.assertEqual(new_nodes[4].text_type, textnode.TextType.TEXT)

    def test_one_start_and_one_end_image(self):
        old_nodes = [textnode.TextNode("![einem image](https://www.image.at) in der Mitte ![noch einem](https://www.image2.at/)", textnode.TextType.TEXT)]
        new_nodes = converter.split_nodes_image(old_nodes)
        self.assertEqual(new_nodes[0].text, "einem image")
        self.assertEqual(new_nodes[0].text_type, textnode.TextType.IMAGE)
        self.assertEqual(new_nodes[0].url, "https://www.image.at")
        self.assertEqual(new_nodes[1].text, " in der Mitte ")
        self.assertEqual(new_nodes[1].text_type, textnode.TextType.TEXT)
        self.assertEqual(new_nodes[2].text, "noch einem")
        self.assertEqual(new_nodes[2].text_type, textnode.TextType.IMAGE)
        self.assertEqual(new_nodes[2].url, "https://www.image2.at/")

    def test_no_image(self):
        old_nodes = [textnode.TextNode("in der Mitte", textnode.TextType.TEXT)]
        new_nodes = converter.split_nodes_link(old_nodes)
        self.assertEqual(new_nodes[0].text, "in der Mitte")
        self.assertEqual(new_nodes[0].text_type, textnode.TextType.TEXT)


class TestConversion(unittest.TestCase):
    def test_example(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = converter.text_to_textnodes(text)
        nodes2 = [
            textnode.TextNode("This is ", textnode.TextType.TEXT),
            textnode.TextNode("text", textnode.TextType.BOLD),
            textnode.TextNode(" with an ", textnode.TextType.TEXT),
            textnode.TextNode("italic", textnode.TextType.ITALIC),
            textnode.TextNode(" word and a ", textnode.TextType.TEXT),
            textnode.TextNode("code block", textnode.TextType.CODE),
            textnode.TextNode(" and an ", textnode.TextType.TEXT),
            textnode.TextNode("obi wan image", textnode.TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            textnode.TextNode(" and a ", textnode.TextType.TEXT),
            textnode.TextNode("link", textnode.TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, nodes2)

    def test_blocks(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = converter.markdown_to_blocks(markdown)
        self.assertEqual(blocks[0], "# This is a heading")
        self.assertEqual(blocks[1], "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.")
        self.assertEqual(blocks[2], """- This is the first list item in a list block
- This is a list item
- This is another list item""")

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = converter.markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_heading_blocks(self):
        self.assertEqual(converter.get_block_type("# test"), converter.BlockType.HEADING)
        self.assertEqual(converter.get_block_type("## test"), converter.BlockType.HEADING)
        self.assertEqual(converter.get_block_type("### test"), converter.BlockType.HEADING)
        self.assertEqual(converter.get_block_type("#### test"), converter.BlockType.HEADING)
        self.assertEqual(converter.get_block_type("##### test"), converter.BlockType.HEADING)
        self.assertEqual(converter.get_block_type("###### test"), converter.BlockType.HEADING)
        self.assertEqual(converter.get_block_type("####### test"), converter.BlockType.PARAGRAPH)

    def test_code_blocks(self):
        self.assertEqual(converter.get_block_type("```\ncode\n```"), converter.BlockType.CODE)
        self.assertEqual(converter.get_block_type("```\ncode```"), converter.BlockType.CODE)

    def test_quote_blocks(self):
        self.assertEqual(converter.get_block_type(">test\n>no"), converter.BlockType.QUOTE)
        self.assertEqual(converter.get_block_type(">\n>"), converter.BlockType.QUOTE)

    def test_quote_ol(self):
        self.assertEqual(converter.get_block_type("1. test\n2. no"), converter.BlockType.ORDERED_LIST)
        self.assertEqual(converter.get_block_type("1. \n2. \n3. \n4. "), converter.BlockType.ORDERED_LIST)

    def test_quote_ul(self):
        self.assertEqual(converter.get_block_type("- test\n- no"), converter.BlockType.UNORDERED_LIST)
        self.assertEqual(converter.get_block_type("- \n- "), converter.BlockType.UNORDERED_LIST)
    
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        html = converter.markdown_to_html(md)
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_heading_block_to_htm(self):
        md = """
# This is **bolded** headline
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""
        html = converter.markdown_to_html(md)
        self.assertEqual(
            html,
            "<div><h1>This is <b>bolded</b> headline\ntext in a p\ntag here</h1><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        html = converter.markdown_to_html(md)
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quoteblock(self):
        md = """
> This is text that _should not_ remain
>the **same** even with inline stuff
"""

        html = converter.markdown_to_html(md)
        self.assertEqual(
            html,
            "<div><blockquote> This is text that <i>should not</i> remain\nthe <b>same</b> even with inline stuff</blockquote></div>",
        )

    def test_ulblock(self):
        md = """
- This is an _unordered list_
- Inline stuff is **adopted**
- With [links](www.link.at)
"""

        html = converter.markdown_to_html(md)
        self.assertEqual(
            html,
            """<div><ul><li>This is an <i>unordered list</i></li><li>Inline stuff is <b>adopted</b></li><li>With <a href="www.link.at">links</a></li></ul></div>""",
        )

    def test_olblock(self):
        md = """
1. This is an _unordered list_
2. Inline stuff is **adopted**
3. With [links](www.link.at)
"""

        html = converter.markdown_to_html(md)
        self.assertEqual(
            html,
            """<div><ol><li>This is an <i>unordered list</i></li><li>Inline stuff is <b>adopted</b></li><li>With <a href="www.link.at">links</a></li></ol></div>""",
        )


if __name__ == "__main__":
    unittest.main()
