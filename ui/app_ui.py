# ui/app_ui.py
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
        "page_bg": "#EEF1F5",     # soft gray like mockup
        "card_bg": "#F7F7F7",     # light card interior
        "card_border": "#D6D6D6",
        "text": "#1F2937",
        "muted": "#374151",

        # Button "gradient" colors (top -> bottom)
        "btn_top": "#2C49F2",
        "btn_bottom": "#1E3FAE",
        "btn_top_sel": "#355CFF",
        "btn_bottom_sel": "#2449CC",
        "btn_text": "#FFFFFF",

        # Disabled look
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
            self.canvas.configure(cursor="hand2")
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

        # Disabled takes precedence
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

            # Slight hover brighten (very subtle)
            if self._hover and not self._selected:
                top = _mix_hex(top, "#FFFFFF", 0.07)
                bottom = _mix_hex(bottom, "#FFFFFF", 0.07)

            text_color = th["btn_text"]

        r = self._radius
        w = self._width
        h = self._height

        # Outer rounded rect in bottom color
        _rounded_rect(self.canvas, 2, 2, w - 2, h - 2, r, fill=bottom, outline="")
        # Top overlay (rounded) for gradient feel
        _rounded_rect(self.canvas, 2, 2, w - 2, int(h * 0.55), r, fill=top, outline="")

        # Subtle highlight line near top (only when enabled)
        if not self._disabled:
            self.canvas.create_line(
                12, 10, w - 12, 10,
                fill=_mix_hex(top, "#FFFFFF", 0.25),
                width=1
            )

        # Text
        self.canvas.create_text(
            w // 2,
            h // 2,
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
    points = [
        x1 + r, y1,
        x2 - r, y1,
        x2, y1,
        x2, y1 + r,
        x2, y2 - r,
        x2, y2,
        x2 - r, y2,
        x1 + r, y2,
        x1, y2,
        x1, y2 - r,
        x1, y1 + r,
        x1, y1
    ]
    return c.create_polygon(points, smooth=True, fill=fill, outline=outline)

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
    current = tk.StringVar(value="sheet")  # sheet | waler

    def th():
        return THEMES[theme_name.get()]

    def apply_theme():
        root.configure(bg=th()["page_bg"])
        topbar.configure(bg=th()["page_bg"])
        screen.configure(bg=th()["page_bg"])

        toggle_btn.configure(
            text="Dark Mode" if theme_name.get() == "light" else "Light Mode",
            bg=th()["card_bg"],
            fg=th()["text"],
            activebackground=th()["card_bg"],
            activeforeground=th()["text"],
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground=th()["card_border"],
            cursor="hand2",
            padx=10,
            pady=6,
        )

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

    toggle_btn = tk.Button(topbar, text="Dark Mode", command=toggle_theme, font=("Arial", 11, "bold"))
    toggle_btn.pack(side=tk.RIGHT, padx=20, pady=12)

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
            cell.grid(row=r, column=c, padx=18, pady=14, sticky="nsew")

            gb = GradientButton(
                cell,
                text=case_name,
                command=lambda n=case_name: select_sheet_case(n),
                width=360,
                height=46,
                radius=14,
                font=("Arial", 12, "bold"),
                theme_getter=th,
                selected=(selected_sheet.get() == case_name),
            )
            gb.pack(pady=(0, 8))
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

        # ✅ Next as GradientButton (no more macOS white button issue)
        next_gb = GradientButton(
            footer,
            text="Next →",
            command=render_waler,
            width=200,
            height=46,
            radius=14,
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
                height=50,
                radius=14,
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
            radius=14,
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
            radius=14,
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
