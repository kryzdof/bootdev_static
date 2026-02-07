import textnode, htmlnode

print(textnode.TextNode("Ein Text", textnode.TextType.TEXT))

print(htmlnode.HTMLNode("p", "some text", None, {
    "href": "https://www.google.com",
    "target": "_blank",
}))

