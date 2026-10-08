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

    def move_node(self, src_parts, dest_parts):
        if not src_parts or not dest_parts:
            return False
        src_parent = self.get_node(src_parts[:-1])
        dest_parent = self.get_node(dest_parts[:-1])
        src_name = src_parts[-1]
        dest_name = dest_parts[-1]
        if not src_parent or src_name not in src_parent.get("children", {}):
            return False
        if not dest_parent:
            return False
        node = src_parent["children"].pop(src_name)
        if "children" not in dest_parent:
            dest_parent["children"] = {}
        dest_parent["children"][dest_name] = node
        return True
