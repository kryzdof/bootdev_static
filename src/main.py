import textnode, htmlnode, converter

print(textnode.TextNode("Ein Text", textnode.TextType.TEXT))

print(htmlnode.HTMLNode("p", "some text", None, {
    "href": "https://www.google.com",
    "target": "_blank",
}))

old_nodes = [textnode.TextNode("Ein text mit **fettem** Zeug", textnode.TextType.TEXT)]

print(converter.split_nodes_delimiter(old_nodes, "**", textnode.TextType.BOLD))

text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
print(converter.extract_markdown_images(text))
