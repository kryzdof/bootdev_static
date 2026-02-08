import textnode, htmlnode, converter

print(textnode.TextNode("Ein Text", textnode.TextType.TEXT))

print(htmlnode.HTMLNode("p", "some text", None, {
    "href": "https://www.google.com",
    "target": "_blank",
}))

old_nodes = [textnode.TextNode("Ein text mit **fettem** Zeug", textnode.TextType.TEXT)]
print(converter.split_nodes_delimiter(old_nodes, "**", textnode.TextType.BOLD))


md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

html = converter.markdown_to_html(md)
print("\n\n\n")
print("-----")
print(html)

blocks = converter.markdown_to_blocks(md)
print(blocks)

