import json

class VFS:
    def __init__(self, json_path=None):
        self.tree = {"type": "dir", "children": {}}
        if json_path:
            self.load_from_json(json_path)

    def load_from_json(self, json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            self.tree = json.load(f)

    def get_node(self, path_parts):
        curr = self.tree
        for part in path_parts:
            if not part or part == ".":
                continue
            if curr.get("type") != "dir" or "children" not in curr:
                return None
            if part not in curr["children"]:
                return None
            curr = curr["children"][part]
        return curr
