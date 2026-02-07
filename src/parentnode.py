from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: [None, dict] = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("tag attribute not set")
        if not self.children:
            raise ValueError("children attribute not set")
        html = f"<{self.tag}{self.props_to_html()}>"
        for c in self.children:
            html += c.to_html()
        html += f"</{self.tag}>"
        return html

    def __repr__(self):
        return f"ParentNode(tag: {self.tag}, kids: {self.children}, props: {self.props_to_html()})"
