print("✅ LOADED NEW app_ui.py")

import tkinter as tk
from tkinter import messagebox

# ---------------------------
# DATA
# ---------------------------
SHEET_PILE_CASES = [
    ("Case I",   "Determine wall moment & top waler"),
    ("Case III", "Determine wall moment and top waler loading after excavation with water on the outside of the wall with two additional walers"),
    ("Case II",  "Determine wall moment and top waler loading after excavation"),
    ("Case IV",  "Determine the moment and minimum length of the cantilever sheet pile"),
    ("Case II W","Determine wall moment and top waler loading after excavation with water on the outside of the wall"),
    ("Case IV W","Determine the moment and minimum length of the cantilever sheet pile with water outside of the sheet pile"),
]

WALER_CASES = [
    ("Waler I",   "Waler for full circle"),
    ("Waler II",  "Waler for semi-circle"),
    ("Waler III", "Waler for segmental arch"),
]

# ---------------------------
# THEME tuned to your mockup colors
# ---------------------------
THEMES = {
    "light": {
        "page_bg": "#F0F4F8",
        "card_bg": "#FFFFFF",
        "card_border": "#E5E7EB",
        "text": "#1F2937",
        "muted": "#374151",

        "btn_top": "#2C49F2",
        "btn_bottom": "#1E3FAE",
        "btn_top_sel": "#355CFF",
        "btn_bottom_sel": "#2449CC",
        "btn_text": "#FFFFFF",

        "disabled_bg": "#D6D6D6",
        "disabled_text": "#6B7280",
    },
    "dark": {
        "page_bg": "#0B1220",
        "card_bg": "#101827",
        "card_border": "#24324A",
        "text": "#EAF0FF",
        "muted": "#A7B3CC",

        "btn_top": "#2C49F2",
        "btn_bottom": "#1E3FAE",
        "btn_top_sel": "#3B82F6",
        "btn_bottom_sel": "#2449CC",
        "btn_text": "#FFFFFF",

        "disabled_bg": "#24324A",
        "disabled_text": "#8FA1C2",
    },
}

# ---------------------------
# Rounded "gradient" button using Canvas
# ---------------------------
class GradientButton(tk.Frame):
    def __init__(
        self,
        parent,
        text,
        command,
        width=360,
        height=46,
        radius=14,
        font=("Arial", 12, "bold"),
        theme_getter=None,
        selected=False,
        disabled=False,
    ):
        super().__init__(parent, bd=0, highlightthickness=0)
        self._command = command
        self._text = text
        self._width = width
        self._height = height
        self._radius = radius
        self._font = font
        self._theme_getter = theme_getter
        self._selected = selected
        self._disabled = disabled
        self._hover = False

        self.canvas = tk.Canvas(self, width=width, height=height, bd=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self._bind_events()
        self.redraw()

    def _bind_events(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Enter>")
        self.canvas.unbind("<Leave>")

        if not self._disabled:
            self.canvas.bind("<Button-1>", lambda e: self._command())
            self.canvas.bind("<Enter>", self._on_enter)
            self.canvas.bind("<Leave>", self._on_leave)
            self.canvas.configure(cursor="")
        else:
            self.canvas.configure(cursor="")

    def set_selected(self, value: bool):
        self._selected = value
        self.redraw()

    def set_disabled(self, value: bool):
        self._disabled = value
        self._bind_events()
        self.redraw()

    def redraw(self):
        self.canvas.delete("all")
        th = self._theme_getter()

        card_bg = th["card_bg"]
        self.canvas.configure(bg=card_bg)
        self.configure(bg=card_bg)

        # Also walk up parent chain to sync bg
        try:
            p = self.master
            while p is not None:
                p.configure(bg=card_bg)
                p = p.master
        except Exception:
            pass
        if self._disabled:
            top = th["disabled_bg"]
            bottom = th["disabled_bg"]
            text_color = th["disabled_text"]
        else:
            if self._selected:
                top = th["btn_top_sel"]
                bottom = th["btn_bottom_sel"]
            else:
                top = th["btn_top"]
                bottom = th["btn_bottom"]

            if self._hover and not self._selected:
                top = _mix_hex(top, "#FFFFFF", 0.07)
                bottom = _mix_hex(bottom, "#FFFFFF", 0.07)

            text_color = th["btn_text"]

        r = self._radius
        w = self._width
        h = self._height

        # Flat solid fill — matches Figma mockup exactly
        _rounded_rect(self.canvas, 0, 0, w, h, r, fill=top, outline="")

        self.canvas.create_text(
            w // 2, h // 2,
            text=self._text,
            fill=text_color,
            font=self._font
        )

    def _on_enter(self, _):
        self._hover = True
        self.redraw()

    def _on_leave(self, _):
        self._hover = False
        self.redraw()


def _rounded_rect(c: tk.Canvas, x1, y1, x2, y2, r, fill, outline):
    # Draw using only rectangles and arcs with matching outline to prevent artifacts
    # Main body
    c.create_rectangle(x1 + r, y1, x2 - r, y2, fill=fill, outline=fill, width=0)
    c.create_rectangle(x1, y1 + r, x2, y2 - r, fill=fill, outline=fill, width=0)
    # Four corners as arcs
    c.create_arc(x1,     y1,     x1+2*r, y1+2*r, start=90,  extent=90, fill=fill, outline=fill, width=0)
    c.create_arc(x2-2*r, y1,     x2,     y1+2*r, start=0,   extent=90, fill=fill, outline=fill, width=0)
    c.create_arc(x1,     y2-2*r, x1+2*r, y2,     start=180, extent=90, fill=fill, outline=fill, width=0)
    c.create_arc(x2-2*r, y2-2*r, x2,     y2,     start=270, extent=90, fill=fill, outline=fill, width=0)

def _mix_hex(a: str, b: str, t: float) -> str:
    a = a.lstrip("#")
    b = b.lstrip("#")
    ar, ag, ab = int(a[0:2], 16), int(a[2:4], 16), int(a[4:6], 16)
    br, bg, bb = int(b[0:2], 16), int(b[2:4], 16), int(b[4:6], 16)
    rr = int(ar + (br - ar) * t)
    rg = int(ag + (bg - ag) * t)
    rb = int(ab + (bb - ab) * t)
    return f"#{rr:02x}{rg:02x}{rb:02x}"

# ---------------------------
# APP
# ---------------------------
def run_app() -> None:
    root = tk.Tk()
    root.title("CofferdamCalc")
    root.geometry("1150x700")
    root.minsize(1050, 650)

    theme_name = tk.StringVar(value="light")
    selected_sheet = tk.StringVar(value="")
    selected_waler = tk.StringVar(value="")
    current = tk.StringVar(value="sheet")

    def th():
        return THEMES[theme_name.get()]

    def apply_theme():
        root.configure(bg=th()["page_bg"])
        topbar.configure(bg=th()["page_bg"])
        screen.configure(bg=th()["page_bg"])

        # Redraw canvas toggle button
        draw_toggle()

        if hasattr(root, "_active_card") and root._active_card is not None:
            root._active_card.configure(
                bg=th()["card_bg"],
                highlightbackground=th()["card_border"],
                highlightthickness=1
            )

        if hasattr(root, "_labels"):
            for lbl, kind in root._labels:
                lbl.configure(
                    bg=th()["card_bg"],
                    fg=th()["text"] if kind == "text" else th()["muted"]
                )

        if hasattr(root, "_desc_labels"):
            for lbl in root._desc_labels:
                lbl.configure(bg=th()["card_bg"], fg=th()["muted"])

        if hasattr(root, "_grad_buttons"):
            for gb in root._grad_buttons:
                gb.redraw()

    def toggle_theme():
        theme_name.set("dark" if theme_name.get() == "light" else "light")
        render()

    # Top bar
    topbar = tk.Frame(root, height=60, bg=th()["page_bg"])
    topbar.pack(fill=tk.X)

    # Canvas-drawn toggle — macOS cannot override canvas item colors
    toggle_canvas = tk.Canvas(
        topbar, width=140, height=36, bd=0, highlightthickness=0, cursor=""
    )
    toggle_canvas.pack(side=tk.RIGHT, padx=20, pady=12)

    def draw_toggle():
        toggle_canvas.delete("all")
        toggle_canvas.configure(bg=th()["page_bg"])
        _rounded_rect(toggle_canvas, 0, 0, 140, 36, 8, fill="#FFFFFF", outline="#CCCCCC")
        label = "🌙 Dark Mode" if theme_name.get() == "light" else "☀ Light Mode"
        toggle_canvas.create_text(70, 18, text=label, fill="#1F2937", font=("Arial", 10, "bold"))

    draw_toggle()
    toggle_canvas.bind("<Button-1>", lambda e: toggle_theme())

    # Screen container
    screen = tk.Frame(root, bg=th()["page_bg"])
    screen.pack(fill=tk.BOTH, expand=True)

    def clear_screen():
        for w in screen.winfo_children():
            w.destroy()
        root._active_card = None
        root._labels = []
        root._desc_labels = []
        root._grad_buttons = []

    def make_card():
        card = tk.Frame(screen, bg=th()["card_bg"], highlightthickness=1, highlightbackground=th()["card_border"])
        card.place(relx=0.5, rely=0.5, anchor="center", width=980, height=560)
        root._active_card = card
        return card

    # --------------- SHEET SCREEN ---------------
    def select_sheet_case(name: str):
        selected_sheet.set(name)
        selected_waler.set("")
        render()

    def render_sheet():
        clear_screen()
        current.set("sheet")
        card = make_card()

        title = tk.Label(card, text="Cofferdam Sheet Pile Analysis", font=("Arial", 26),
                         bg=th()["card_bg"], fg=th()["text"])
        title.pack(pady=(20, 22))
        root._labels.append((title, "text"))

        grid = tk.Frame(card, bg=th()["card_bg"])
        grid.pack(fill=tk.BOTH, expand=True, padx=30)

        left_col = [SHEET_PILE_CASES[0], SHEET_PILE_CASES[2], SHEET_PILE_CASES[4]]
        right_col = [SHEET_PILE_CASES[1], SHEET_PILE_CASES[3], SHEET_PILE_CASES[5]]

        def case_block(parent, case_name, desc, r, c):
            cell = tk.Frame(parent, bg=th()["card_bg"])
            cell.grid(row=r, column=c, padx=18, pady=6, sticky="nsew")

            gb = GradientButton(
                cell,
                text=case_name,
                command=lambda n=case_name: select_sheet_case(n),
                width=360,
                height=52,
                radius=26,
                font=("Arial", 12, "bold"),
                theme_getter=th,
                selected=(selected_sheet.get() == case_name),
            )
            gb.pack(pady=(0, 4))
            root._grad_buttons.append(gb)

            d = tk.Label(cell, text=desc, font=("Arial", 10), wraplength=380, justify="center",
                         bg=th()["card_bg"], fg=th()["muted"])
            d.pack()
            root._desc_labels.append(d)

        for r in range(3):
            case_block(grid, left_col[r][0], left_col[r][1], r, 0)
            case_block(grid, right_col[r][0], right_col[r][1], r, 1)

        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)
        for r in range(3):
            grid.grid_rowconfigure(r, weight=1)

        footer = tk.Frame(card, bg=th()["card_bg"])
        footer.pack(fill=tk.X, pady=(10, 16), padx=30)

        status = tk.Label(
            footer,
            text=f"Selected: {selected_sheet.get() or '(none)'}",
            font=("Arial", 11, "bold"),
            bg=th()["card_bg"],
            fg=th()["text"],
        )
        status.pack(side=tk.LEFT)
        root._labels.append((status, "text"))

        next_gb = GradientButton(
            footer,
            text="Next →",
            command=render_waler,
            width=200,
            height=46,
            radius=23,
            font=("Arial", 12, "bold"),
            theme_getter=th,
        )
        next_gb.pack(side=tk.RIGHT)
        root._grad_buttons.append(next_gb)
        next_gb.set_disabled(not bool(selected_sheet.get()))

        apply_theme()

    # --------------- WALER SCREEN ---------------
    def select_waler_case(name: str):
        selected_waler.set(name)
        render()

    def render_waler():
        if not selected_sheet.get():
            return
        clear_screen()
        current.set("waler")
        card = make_card()

        title = tk.Label(card, text="Select Waler Case", font=("Arial", 24, "bold"),
                         bg=th()["card_bg"], fg=th()["text"])
        title.pack(pady=(26, 8))
        root._labels.append((title, "text"))

        sub = tk.Label(card, text=f"Sheet Pile Case: {selected_sheet.get()}",
                       font=("Arial", 12), bg=th()["card_bg"], fg=th()["muted"])
        sub.pack(pady=(0, 22))
        root._labels.append((sub, "muted"))

        area = tk.Frame(card, bg=th()["card_bg"])
        area.pack(fill=tk.X, padx=70)

        for w_name, w_desc in WALER_CASES:
            row = tk.Frame(area, bg=th()["card_bg"])
            row.pack(fill=tk.X, pady=12)

            gb = GradientButton(
                row,
                text=w_name,
                command=lambda n=w_name: select_waler_case(n),
                width=820,
                height=52,
                radius=26,
                font=("Arial", 12, "bold"),
                theme_getter=th,
                selected=(selected_waler.get() == w_name),
            )
            gb.pack(pady=(0, 6))
            root._grad_buttons.append(gb)

            d = tk.Label(row, text=w_desc, font=("Arial", 10),
                         bg=th()["card_bg"], fg=th()["muted"])
            d.pack()
            root._desc_labels.append(d)

        footer = tk.Frame(card, bg=th()["card_bg"])
        footer.pack(fill=tk.X, pady=(18, 16), padx=70)

        back_gb = GradientButton(
            footer,
            text="← Back",
            command=render_sheet,
            width=200,
            height=46,
            radius=23,
            font=("Arial", 12, "bold"),
            theme_getter=th,
        )
        back_gb.pack(side=tk.LEFT)
        root._grad_buttons.append(back_gb)

        cont_gb = GradientButton(
            footer,
            text="Continue →",
            command=lambda: messagebox.showinfo(
                "Selection Confirmed",
                f"Sheet Pile: {selected_sheet.get()}\nWaler: {selected_waler.get()}",
            ),
            width=220,
            height=46,
            radius=23,
            font=("Arial", 12, "bold"),
            theme_getter=th,
        )
        cont_gb.pack(side=tk.RIGHT)
        root._grad_buttons.append(cont_gb)
        cont_gb.set_disabled(not bool(selected_waler.get()))

        apply_theme()

    def render():
        apply_theme()
        if current.get() == "sheet":
            render_sheet()
        else:
            render_waler()

    render_sheet()
    root.mainloop()


if __name__ == "__main__":
    run_app()