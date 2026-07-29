"""Standalone Tk JSON editor for every Humanlike v2 configuration field."""

from __future__ import annotations

import argparse
import json
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from players.humanlike.settings_service import default_config_path, read_raw, save_raw, validate_raw


class SettingsWindow:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.root = tk.Tk()
        self.root.title("Humanlike AI v2 — 全参数设置")
        self.root.geometry("920x720")
        self.root.configure(bg="#0d2818")
        tk.Label(self.root, text="Humanlike AI v2 全参数设置", bg="#0d2818", fg="#fff3c4", font=("TkDefaultFont", 16, "bold")).pack(fill="x", padx=12, pady=(10, 2))
        tk.Label(self.root, text="覆盖 GP-001–027、S0–S3 玩家画像、版本与 seed；规范锁定项无法通过校验保存。所有修改下局生效。", bg="#0d2818", fg="#9fd8bd", wraplength=880, justify="left").pack(fill="x", padx=12, pady=(0, 8))
        frame = tk.Frame(self.root, bg="#12261c")
        frame.pack(fill="both", expand=True, padx=12, pady=4)
        scroll = tk.Scrollbar(frame)
        scroll.pack(side="right", fill="y")
        self.text = tk.Text(frame, undo=True, wrap="none", bg="#102019", fg="#e8f5e9", insertbackground="white", font=("Courier", 11), yscrollcommand=scroll.set)
        self.text.pack(fill="both", expand=True)
        scroll.config(command=self.text.yview)
        bar = tk.Frame(self.root, bg="#0d2818")
        bar.pack(fill="x", padx=12, pady=10)
        for label, fn in (("重新载入", self.reload), ("校验", self.validate), ("保存", self.save), ("导入…", self.import_file), ("导出…", self.export_file)):
            tk.Button(bar, text=label, command=fn, bg="#256d45", fg="white", padx=12).pack(side="left", padx=4)
        tk.Button(bar, text="关闭", command=self.root.destroy, bg="#5b4030", fg="white", padx=12).pack(side="right", padx=4)
        self.status = tk.StringVar(value=str(path))
        tk.Label(self.root, textvariable=self.status, bg="#0d2818", fg="#b0bec5", anchor="w").pack(fill="x", padx=12, pady=(0, 8))
        self.reload()

    def _data(self):
        return json.loads(self.text.get("1.0", "end"))

    def reload(self):
        self.text.delete("1.0", "end")
        self.text.insert("1.0", json.dumps(read_raw(self.path), ensure_ascii=False, indent=2))
        self.status.set(f"已载入：{self.path}")

    def validate(self):
        try:
            cfg = validate_raw(self._data(), target=self.path)
            self.status.set(f"校验通过 · hash {cfg.config_hash[:12]}")
            return True
        except Exception as exc:
            messagebox.showerror("参数校验失败", str(exc), parent=self.root)
            self.status.set(f"校验失败：{exc}")
            return False

    def save(self):
        try:
            cfg = save_raw(self._data(), self.path)
        except Exception as exc:
            messagebox.showerror("保存失败", str(exc), parent=self.root)
            return
        self.status.set(f"保存成功，下局生效 · hash {cfg.config_hash[:12]}")

    def import_file(self):
        name = filedialog.askopenfilename(filetypes=[("JSON", "*.json")], parent=self.root)
        if name:
            data = read_raw(name)
            validate_raw(data, target=self.path)
            self.text.delete("1.0", "end"); self.text.insert("1.0", json.dumps(data, ensure_ascii=False, indent=2))

    def export_file(self):
        name = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")], parent=self.root)
        if name:
            Path(name).write_text(json.dumps(self._data(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def run(self): self.root.mainloop()


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--config")
    args = parser.parse_args(); SettingsWindow(Path(args.config) if args.config else default_config_path()).run(); return 0


if __name__ == "__main__": raise SystemExit(main())
