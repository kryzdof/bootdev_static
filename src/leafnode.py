from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag: [None, str], value: str, props: [None, dict] = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self) -> str:
        if self.tag == "img":
            return f"<img {self.props_to_html()}>"
        if not self.value:
            raise ValueError("value attribute not set")
        if not self.tag:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self) -> str:
        return f"LeafNode(tag: {self.tag}, value: {self.value}, props: {self.props_to_html()})"

