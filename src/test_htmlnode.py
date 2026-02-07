import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_notImpl(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)

    def test_neq(self):
        node = HTMLNode("p")
        node2 = HTMLNode()
        self.assertNotEqual(node, node2)

    def test_eq(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertNotEqual(node, node2)

    def test_initialization(self):
        n = HTMLNode("p", "some text", None, {"attr": "value"})
        self.assertEqual("p", n.tag)
        self.assertEqual("some text", n.value)
        self.assertEqual(None, n.children)
        self.assertEqual({"attr": "value"}, n.props)

    def test_props_to_html(self):
        n = HTMLNode(None, None, None, {"href": "https://www.google.com","target": "_blank",})
        self.assertEqual(n.props_to_html(), ' href="https://www.google.com" target="_blank"')

if __name__ == "__main__":
    unittest.main()
