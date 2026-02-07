import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html_p(self):
        node = LeafNode("p", "test")
        self.assertEqual(node.to_html(), '<p>test</p>')

    def test_to_html_a(self):
        n = LeafNode("a", "a link", {"href": "https://www.google.com","target": "_blank"})
        self.assertEqual(n.to_html(), '<a href="https://www.google.com" target="_blank">a link</a>')

    def test_to_html_h1(self):
        n = LeafNode("h1", "a headline", {"href": "https://www.google.com","target": "_blank"})
        self.assertEqual(n.to_html(), '<h1 href="https://www.google.com" target="_blank">a headline</h1>')

    def test_neq(self):
        node = LeafNode("p", None)
        node2 = LeafNode("a", None)
        self.assertNotEqual(node, node2)

    def test_eq(self):
        node = LeafNode("p", "someText")
        node2 = LeafNode("p", "someText")
        self.assertNotEqual(node, node2)

    def test_initialization(self):
        n = LeafNode("p", "some text", {"attr": "value"})
        self.assertEqual("p", n.tag)
        self.assertEqual("some text", n.value)
        self.assertEqual(None, n.children)
        self.assertEqual({"attr": "value"}, n.props)

    def test_props_to_html(self):
        n = LeafNode(None, None, {"href": "https://www.google.com","target": "_blank"})
        self.assertEqual(n.props_to_html(), ' href="https://www.google.com" target="_blank"')

if __name__ == "__main__":
    unittest.main()
