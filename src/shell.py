import os
import shlex

class ShellEngine:
    def __init__(self, vfs):
        self.vfs = vfs
        self.cwd = []
        self.history_list = []

    def parse_line(self, line):
        expanded = os.path.expandvars(line)
        return shlex.split(expanded)

    def execute(self, line):
        line = line.strip()
        if not line:
            return ""
        self.history_list.append(line)
        
        try:
            args = self.parse_line(line)
        except Exception as e:
            return f"Parse error: {e}"

        if not args:
            return ""

        cmd = args[0]
        cmd_args = args[1:]

        if cmd == "exit":
            return "EXIT"
        elif cmd == "ls":
            node = self.vfs.get_node(self.cwd)
            if node and node.get("type") == "dir":
                return "  ".join(node.get("children", {}).keys())
            return ""
        elif cmd == "cd":
            if not cmd_args or cmd_args[0] == "/":
                self.cwd = []
            elif cmd_args[0] == "..":
                if self.cwd:
                    self.cwd.pop()
            else:
                target = self.cwd + cmd_args[0].split("/")
                node = self.vfs.get_node(target)
                if node and node.get("type") == "dir":
                    self.cwd = target
                else:
                    return f"cd: {cmd_args[0]}: No such directory"
            return ""
        elif cmd == "cat":
            if not cmd_args:
                return "cat: missing operand"
            target = self.cwd + cmd_args[0].split("/")
            node = self.vfs.get_node(target)
            if node and node.get("type") == "file":
                return node.get("content", "")
            return f"cat: {cmd_args[0]}: No such file"
        elif cmd == "history":
            return "\n".join(f"{i+1}  {c}" for i, c in enumerate(self.history_list))
        elif cmd == "head":
            if not cmd_args:
                return "head: missing operand"
            target = self.cwd + cmd_args[0].split("/")
            node = self.vfs.get_node(target)
            if node and node.get("type") == "file":
                lines = node.get("content", "").splitlines()
                return "\n".join(lines[:10])
            return f"head: {cmd_args[0]}: No such file"
        elif cmd == "mv":
            if len(cmd_args) < 2:
                return "mv: missing file operand"
            src = self.cwd + cmd_args[0].split("/")
            dest = self.cwd + cmd_args[1].split("/")
            if self.vfs.move_node(src, dest):
                return ""
            return "mv: failed to move"
        elif cmd == "vfs-load":
            if not cmd_args:
                return "vfs-load: missing path"
            try:
                self.vfs.load_from_json(cmd_args[0])
                self.cwd = []
                return "VFS successfully loaded"
            except Exception as e:
                return f"vfs-load error: {e}"
        else:
            return f"{cmd}: command not found"
