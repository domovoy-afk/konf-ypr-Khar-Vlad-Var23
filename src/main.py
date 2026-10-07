import argparse
import getpass
import json
import os
import shlex
import socket
import sys
import tkinter as tk
from tkinter import scrolledtext

class ShellEngine:
    def __init__(self):
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
        elif cmd in ("ls", "cd"):
            return f"{cmd} {' '.join(cmd_args)}".strip()
        else:
            return f"{cmd}: command not found"

class EmulatorGUI:
    def __init__(self, root, engine):
        self.root = root
        self.engine = engine

        username = getpass.getuser()
        hostname = socket.gethostname()
        self.root.title(f"Эмулятор [{username}@{hostname}]")
        self.root.geometry("650x350")

        self.output_area = scrolledtext.ScrolledText(
            root, state="disabled", bg="black", fg="white", font=("Consolas", 11)
        )
        self.output_area.pack(fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(root, bg="#1e1e1e", fg="white", font=("Consolas", 11))
        self.entry.pack(fill=tk.X)
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus()

        self.write_output(f"Welcome to Emulator [{username}@{hostname}]\n\n")

    def write_output(self, text):
        self.output_area.config(state="normal")
        self.output_area.insert(tk.END, text)
        self.output_area.config(state="disabled")
        self.output_area.see(tk.END)

    def on_enter(self, event):
        command = self.entry.get()
        self.entry.delete(0, tk.END)
        self.write_output(f"$ {command}\n")

        res = self.engine.execute(command)
        if res == "EXIT":
            self.root.destroy()
        elif res:
            self.write_output(f"{res}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--vfs", help="Path to VFS JSON file", default=None)
    parser.add_argument("--script", help="Path to startup script", default=None)
    args = parser.parse_args()

    print(f"Debug Config -> VFS: {args.vfs}, Script: {args.script}")

    engine = ShellEngine()

    if args.script:
        try:
            with open(args.script, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        res = engine.execute(line)
                        if "not found" in res or "error" in res.lower():
                            print(f"Script Execution Error: {res}")
                            sys.exit(1)
        except Exception as e:
            print(f"Failed to read script: {e}")
            sys.exit(1)

    root = tk.Tk()
    app = EmulatorGUI(root, engine)
    root.mainloop()
