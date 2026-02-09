import unittest

from main import extract_title


class TestMain(unittest.TestCase):
    def test_extract_title(self):
        md = """not at the start\n# my title\n# another title\n## even better\n# more!"""
        title = extract_title(md)
        self.assertEqual(title, 'my title')

    def test_extract_title2(self):
        md = """# not at the start"""
        title = extract_title(md)
        self.assertEqual(title, 'not at the start')

    def test_extract_title_error(self):
        md = """not at the start"""
        with self.assertRaises(AttributeError):
            title = extract_title(md)

if __name__ == "__main__":
    unittest.main()
