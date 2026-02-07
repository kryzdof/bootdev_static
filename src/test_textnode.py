import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This s a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        leaf_node = node.to_LeafNode()
        self.assertEqual(leaf_node.tag, None)
        self.assertEqual(leaf_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        leaf_node = node.to_LeafNode()
        self.assertEqual(leaf_node.tag, "b")
        self.assertEqual(leaf_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        leaf_node = node.to_LeafNode()
        self.assertEqual(leaf_node.tag, "i")
        self.assertEqual(leaf_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        leaf_node = node.to_LeafNode()
        self.assertEqual(leaf_node.tag, "code")
        self.assertEqual(leaf_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "www.link.at")
        leaf_node = node.to_LeafNode()
        self.assertEqual(leaf_node.tag, "a")
        self.assertEqual(leaf_node.value, "This is a link node")
        self.assertEqual(leaf_node.props, {"href": "www.link.at"})
        self.assertEqual(leaf_node.props_to_html(), ' href="www.link.at"')

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "www.image.at")
        leaf_node = node.to_LeafNode()
        self.assertEqual(leaf_node.tag, "img")
        self.assertEqual(leaf_node.value, None)
        self.assertEqual(leaf_node.props, {"alt": "This is an image node", "src": "www.image.at"})
        self.assertEqual(leaf_node.props_to_html(), ' src="www.image.at" alt="This is an image node"')


if __name__ == "__main__":
    unittest.main()
