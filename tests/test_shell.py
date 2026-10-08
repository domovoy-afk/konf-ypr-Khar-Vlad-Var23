import unittest
from src.vfs import VFS
from src.shell import ShellEngine

class TestShellEngine(unittest.TestCase):
    def setUp(self):
        self.vfs = VFS()
        self.vfs.tree = {
            "type": "dir",
            "children": {
                "file1.txt": {"type": "file", "content": "Line 1\nLine 2"},
                "docs": {"type": "dir", "children": {}}
            }
        }
        self.engine = ShellEngine(self.vfs)

    def test_ls(self):
        res = self.engine.execute("ls")
        self.assertIn("file1.txt", res)
        self.assertIn("docs", res)

    def test_cd(self):
        self.engine.execute("cd docs")
        self.assertEqual(self.engine.cwd, ["docs"])

    def test_cat(self):
        res = self.engine.execute("cat file1.txt")
        self.assertEqual(res, "Line 1\nLine 2")

    def test_head(self):
        res = self.engine.execute("head file1.txt")
        self.assertEqual(res, "Line 1\nLine 2")

    def test_history(self):
        self.engine.execute("ls")
        res = self.engine.execute("history")
        self.assertIn("ls", res)

if __name__ == "__main__":
    unittest.main()
