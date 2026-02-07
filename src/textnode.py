from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT = None
    BOLD = "b"
    ITALIC = "i"
    CODE = "code"
    LINK = "a"
    IMAGE = "img"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: [None,str] =None):
        if not isinstance(text_type, TextType):
            raise Exception("wrong text_type type")
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        if self.text != other.text:
            return False
        if self.text_type != other.text_type:
            return False
        if self.url != other.url:
            return False
        return True

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    def to_LeafNode(self) -> LeafNode:
        match self.text_type:
            case TextType.IMAGE:
                return LeafNode(self.text_type.value, None, {"src": self.url, "alt": self.text})
            case TextType.LINK:
                return LeafNode(self.text_type.value, self.text, {"href": self.url})
        return LeafNode(self.text_type.value, self.text, self.url)

