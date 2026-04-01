#!/usr/bin/env python3
"""
Quantex GUI Generator
Pokretanje: python tools/gui.py
"""
from __future__ import annotations
import os
import re
import subprocess
import sys
import threading
import webbrowser
from pathlib import Path

import tkinter as tk

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

ROOT_DIR = Path(__file__).parent.parent
TOOLS_DIR = Path(__file__).parent
OUTPUT_DIR = TOOLS_DIR / "output"
BLOG_DIR = ROOT_DIR / "blog"

# ── Brand colors ──────────────────────────────────────────────────────────────
BG      = "#060912"
BG2     = "#0d1322"
BG3     = "#0f1928"
ACCENT  = "#3b82f6"
CYAN    = "#06b6d4"
TEXT    = "#f1f5f9"
TEXT2   = "#94a3b8"
MUTED   = "#4b5563"
BORDER  = "#1a2535"
SUCCESS = "#10b981"
ERROR   = "#ef4444"
TERM_FG = "#86efac"  # terminal green


class QuantexApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quantex Generator")
        self.geometry("1000x820")
        self.minsize(800, 600)
        self.configure(bg=BG)

        self._slug: str | None = None
        self._images: list = []   # PhotoImage refs to prevent GC
        self._process: subprocess.Popen | None = None

        self._build_ui()
        self._check_api_key()

    # ── UI build ──────────────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Header ────────────────────────────────────────────
        hdr = tk.Frame(self, bg=BG, padx=36, pady=22)
        hdr.pack(fill="x")

        title_row = tk.Frame(hdr, bg=BG)
        title_row.pack(fill="x")
        tk.Label(title_row, text="QUANTEX", bg=BG, fg=TEXT,
                 font=("Helvetica", 22, "bold")).pack(side="left")
        tk.Label(title_row, text="  Blog & Instagram Karuzel Generator",
                 bg=BG, fg=TEXT2, font=("Helvetica", 12)).pack(side="left", pady=2)

        self.api_lbl = tk.Label(hdr, text="", bg=BG, font=("Helvetica", 9))
        self.api_lbl.pack(anchor="w", pady=(4, 0))

        # ── Separator ─────────────────────────────────────────
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

        # ── Input section ─────────────────────────────────────
        inp = tk.Frame(self, bg=BG2, padx=36, pady=26)
        inp.pack(fill="x")

        tk.Label(inp, text="Tema", bg=BG2, fg=TEXT2,
                 font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 6))

        entry_wrap = tk.Frame(inp, bg=ACCENT, padx=1, pady=1)
        entry_wrap.pack(fill="x")
        self.topic_entry = tk.Entry(
            entry_wrap,
            bg=BG3, fg=TEXT, insertbackground=TEXT,
            font=("Helvetica", 13), relief="flat",
            highlightthickness=0, bd=10,
        )
        self.topic_entry.pack(fill="x")
        self.topic_entry.bind("<Return>", lambda _: self._generate())

        # Checkboxes
        chk_row = tk.Frame(inp, bg=BG2)
        chk_row.pack(anchor="w", pady=(16, 0))

        self.blog_var = tk.BooleanVar(value=True)
        self.carousel_var = tk.BooleanVar(value=True)

        for text, var in [("Blog post", self.blog_var), ("Instagram karuzel", self.carousel_var)]:
            tk.Checkbutton(
                chk_row, text=text, variable=var,
                bg=BG2, fg=TEXT2,
                activebackground=BG2, activeforeground=TEXT,
                selectcolor=BG3,
                font=("Helvetica", 11), bd=0,
            ).pack(side="left", padx=(0, 28))

        # Button row
        btn_row = tk.Frame(inp, bg=BG2)
        btn_row.pack(anchor="w", pady=(20, 0))

        self.gen_btn = tk.Button(
            btn_row, text="Generišite",
            command=self._generate,
            bg=ACCENT, fg="white",
            activebackground="#2563eb", activeforeground="white",
            font=("Helvetica", 12, "bold"),
            relief="flat", bd=0,
            padx=32, pady=10,
            cursor="hand2",
        )
        self.gen_btn.pack(side="left")

        self.status_lbl = tk.Label(btn_row, text="", bg=BG2,
                                   font=("Helvetica", 10))
        self.status_lbl.pack(side="left", padx=16)

        # ── Separator ─────────────────────────────────────────
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

        # ── Terminal ──────────────────────────────────────────
        term_hdr = tk.Frame(self, bg=BG, padx=36, pady=14)
        term_hdr.pack(fill="x")
        tk.Label(term_hdr, text="Terminal output", bg=BG, fg=MUTED,
                 font=("Courier", 9, "bold")).pack(anchor="w")

        term_wrap = tk.Frame(self, bg=BG3, padx=2, pady=2)
        term_wrap.pack(fill="both", expand=True, padx=36, pady=(0, 14))

        self.terminal = tk.Text(
            term_wrap,
            bg=BG3, fg=TERM_FG,
            insertbackground=TEXT,
            font=("Courier", 10),
            relief="flat", bd=10,
            wrap="word",
            state="disabled",
        )
        vbar = tk.Scrollbar(term_wrap, command=self.terminal.yview, bg=BG2,
                            troughcolor=BG3)
        self.terminal.configure(yscrollcommand=vbar.set)
        vbar.pack(side="right", fill="y")
        self.terminal.pack(fill="both", expand=True)

        # ── Results (populated after generation) ──────────────
        self.results_frame = tk.Frame(self, bg=BG, padx=36)
        self.results_frame.pack(fill="x", pady=(0, 20))

    # ── API key check ─────────────────────────────────────────────────────────

    def _check_api_key(self):
        if os.environ.get("ANTHROPIC_API_KEY"):
            self.api_lbl.configure(
                text="API ključ: pronađen",
                fg=SUCCESS,
            )
        else:
            self.api_lbl.configure(
                text="UPOZORENJE: ANTHROPIC_API_KEY nije postavljen. Generisanje neće raditi.",
                fg=ERROR,
            )

    # ── Generation ────────────────────────────────────────────────────────────

    def _generate(self):
        topic = self.topic_entry.get().strip()
        if not topic:
            self._set_status("Unesite temu.", error=True)
            return

        if not self.blog_var.get() and not self.carousel_var.get():
            self._set_status("Izaberite bar jednu opciju.", error=True)
            return

        # Reset
        self._slug = None
        self._images.clear()
        for w in self.results_frame.winfo_children():
            w.destroy()
        self._terminal_clear()
        self.gen_btn.configure(state="disabled", text="Generišem...")
        self._set_status("Pokrećem...", error=False)

        cmd = [sys.executable, str(TOOLS_DIR / "generate.py"), "--topic", topic]
        if self.blog_var.get() and not self.carousel_var.get():
            cmd.append("--blog-only")
        elif self.carousel_var.get() and not self.blog_var.get():
            cmd.append("--carousel-only")

        threading.Thread(
            target=self._run,
            args=(cmd, self.blog_var.get(), self.carousel_var.get()),
            daemon=True,
        ).start()

    def _run(self, cmd: list, want_blog: bool, want_carousel: bool):
        try:
            env = os.environ.copy()
            self._process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1,
                cwd=str(TOOLS_DIR),
                env=env,
            )
            for line in self._process.stdout:
                line = line.rstrip()
                self._term_append(line)
                m = re.search(r"^Slug:\s+(.+)$", line)
                if m:
                    self._slug = m.group(1).strip()

            self._process.wait()
            rc = self._process.returncode

            if rc == 0:
                self.after(0, self._on_done, want_blog, want_carousel)
            else:
                self.after(0, self._on_error, f"Greška, exit code {rc}")
        except Exception as exc:
            self.after(0, self._on_error, str(exc))

    def _on_done(self, want_blog: bool, want_carousel: bool):
        self.gen_btn.configure(state="normal", text="Generišite")
        self._set_status("Gotovo.", error=False, color=SUCCESS)
        self._show_results(want_blog, want_carousel)

    def _on_error(self, msg: str):
        self.gen_btn.configure(state="normal", text="Generišite")
        self._set_status(msg, error=True)

    # ── Results section ───────────────────────────────────────────────────────

    def _show_results(self, want_blog: bool, want_carousel: bool):
        f = self.results_frame
        tk.Frame(f, bg=BORDER, height=1).pack(fill="x", pady=(0, 16))

        # Blog post link
        if want_blog and self._slug:
            blog_path = BLOG_DIR / f"{self._slug}.html"
            if blog_path.exists():
                row = tk.Frame(f, bg=BG)
                row.pack(fill="x", pady=(0, 10))

                tk.Label(row, text="Blog post:", bg=BG, fg=MUTED,
                         font=("Helvetica", 10, "bold")).pack(side="left")

                link = tk.Label(row, text=f"  blog/{self._slug}.html",
                                bg=BG, fg=ACCENT, font=("Helvetica", 10),
                                cursor="hand2")
                link.pack(side="left")
                link.bind("<Button-1>", lambda _: webbrowser.open(f"file://{blog_path}"))

                tk.Button(
                    row, text="Otvori u browseru",
                    command=lambda: webbrowser.open(f"file://{blog_path}"),
                    bg=BG3, fg=TEXT,
                    activebackground=ACCENT, activeforeground="white",
                    font=("Helvetica", 9), relief="flat",
                    padx=12, pady=4, cursor="hand2",
                ).pack(side="left", padx=(12, 0))

        # Carousel images
        if want_carousel and self._slug:
            out_dir = OUTPUT_DIR / self._slug
            pngs = sorted(out_dir.glob("slide_*.png")) if out_dir.exists() else []

            if pngs:
                tk.Label(f, text=f"Karuzel slajdovi  ({len(pngs)})",
                         bg=BG, fg=MUTED,
                         font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(6, 10))

                # Canvas + horizontal scrollbar
                outer = tk.Frame(f, bg=BG)
                outer.pack(fill="x")

                canvas = tk.Canvas(outer, bg=BG, height=230,
                                   highlightthickness=0)
                hbar = tk.Scrollbar(outer, orient="horizontal",
                                    command=canvas.xview,
                                    bg=BG2, troughcolor=BG3)
                canvas.configure(xscrollcommand=hbar.set)

                inner = tk.Frame(canvas, bg=BG)
                canvas.create_window((0, 0), window=inner, anchor="nw")

                for i, png in enumerate(pngs):
                    self._add_thumb(inner, png, i + 1)

                inner.update_idletasks()
                canvas.configure(scrollregion=canvas.bbox("all"))
                canvas.pack(fill="x", expand=True)
                hbar.pack(fill="x")

                # Open folder button
                tk.Button(
                    f, text=f"Otvori folder  →  tools/output/{self._slug}/",
                    command=lambda: subprocess.Popen(["xdg-open", str(out_dir)]),
                    bg=BG3, fg=TEXT2,
                    activebackground=BG2, activeforeground=TEXT,
                    font=("Helvetica", 9), relief="flat",
                    padx=12, pady=6, cursor="hand2", anchor="w",
                ).pack(anchor="w", pady=(10, 0))

    def _add_thumb(self, parent: tk.Frame, png: Path, num: int):
        cell = tk.Frame(parent, bg=BG2, padx=3, pady=3)
        cell.pack(side="left", padx=8)

        if HAS_PIL:
            img = Image.open(png)
            img.thumbnail((180, 180))
            photo = ImageTk.PhotoImage(img)
            self._images.append(photo)

            lbl = tk.Label(cell, image=photo, bg=BG2, cursor="hand2")
            lbl.pack()
            lbl.bind("<Button-1>", lambda _, p=png: subprocess.Popen(["xdg-open", str(p)]))
        else:
            tk.Label(cell, text=f"[Slajd {num}]", bg=BG2, fg=TEXT2,
                     font=("Courier", 9), width=18, height=10).pack()

        tk.Label(cell, text=f"Slajd {num}", bg=BG2, fg=MUTED,
                 font=("Helvetica", 8)).pack(pady=(3, 0))

    # ── Terminal helpers ──────────────────────────────────────────────────────

    def _terminal_clear(self):
        self.terminal.configure(state="normal")
        self.terminal.delete("1.0", "end")
        self.terminal.configure(state="disabled")

    def _term_append(self, text: str):
        self.after(0, self._term_append_safe, text)

    def _term_append_safe(self, text: str):
        self.terminal.configure(state="normal")
        self.terminal.insert("end", text + "\n")
        self.terminal.see("end")
        self.terminal.configure(state="disabled")

    def _set_status(self, msg: str, error: bool = False, color: str | None = None):
        c = color or (ERROR if error else TEXT2)
        self.status_lbl.configure(text=msg, fg=c)


if __name__ == "__main__":
    app = QuantexApp()
    app.mainloop()
