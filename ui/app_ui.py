"""
Project: CofferdamCalc
File: app_ui.py
Authors: Adetola Aladekoba and Rylan Weldon
Date Last Modified: 3/1/2026

Description:
This portion of the program is created to provide a UI to the user and allow them to select
sheet pile analysis cases and walter configurations through a graphic interface with theme support.

Changes Made: 
02/22/2026
Author: Rylan Weldon

Refactored the application from the function based structure into a class based and object oriented design
by implementing the CofferdamApp class. The CofferdamApp class allowed all of the application states (theme and
user selections) into different instance variables instead of attaching different custom attributes to the root.
Also the data structures for both the sheet pile and waler case data from lists of tuples into dictionaries to improve effeciency
in lookups and to improve readability. Also created a render method to reduce redundent logic in the rendering process
and used @property to access the current theme. 
"""
import tkinter as tk
from tkinter import messagebox

# ---------------------------
# DATA
# ---------------------------
SHEET_PILE_CASES = {
    "Case I": "Determine wall moment & top waler",
    "Case III": "Determine wall moment and top waler loading after excavation with water on the outside of the wall with two additional walers",
    "Case II": "Determine wall moment and top waler loading after excavation",
    "Case IV": "Determine the moment and minimum length of the cantilever sheet pile",
    "Case II W": "Determine wall moment and top waler loading after excavation with water on the outside of the wall",
    "Case IV W": "Determine the moment and minimum length of the cantilever sheet pile with water outside of the sheet pile",
}

WALER_CASES = {
    "Waler I": "Waler for full circle",
    "Waler II": "Waler for semi-circle",
    "Waler III": "Waler for segmental arch",
}

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
        theme_getter,
        width=360,
        height=46,
        radius=14,
        font=("Arial", 12, "bold"),
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

        self.canvas = tk.Canvas(
            self,
            width=width,
            height=height,
            bd=0,
            highlightthickness=0,
            cursor="hand2",
        )
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

        self.canvas.configure(bg=th["card_bg"])
        self.configure(bg=th["card_bg"])

        if self._disabled:
            fill_color = th["disabled_bg"]
            text_color = th["disabled_text"]
        else:
            if self._selected:
                fill_color = th["btn_top_sel"]
            else:
                fill_color = th["btn_top"]

            if self._hover and not self._selected:
                fill_color = blend_colors(fill_color, "#FFFFFF", 0.07)

            text_color = th["btn_text"]

        r = self._radius
        w = self._width
        h = self._height

        rounded_rect(self.canvas, 0, 0, w, h, r, fill=fill_color, outline="")
        self.canvas.create_text(
            w // 2,
            h // 2,
            text=self._text,
            fill=text_color,
            font=self._font,
        )

    def _on_enter(self, _):
        self._hover = True
        self.redraw()

    def _on_leave(self, _):
        self._hover = False
        self.redraw()


def rounded_rect(c: tk.Canvas, x1, y1, x2, y2, r, fill, outline):
    c.create_rectangle(x1 + r, y1, x2 - r, y2, fill=fill, outline=fill, width=0)
    c.create_rectangle(x1, y1 + r, x2, y2 - r, fill=fill, outline=fill, width=0)
    c.create_arc(x1, y1, x1 + 2 * r, y1 + 2 * r, start=90, extent=90, fill=fill, outline=fill, width=0)
    c.create_arc(x2 - 2 * r, y1, x2, y1 + 2 * r, start=0, extent=90, fill=fill, outline=fill, width=0)
    c.create_arc(x1, y2 - 2 * r, x1 + 2 * r, y2, start=180, extent=90, fill=fill, outline=fill, width=0)
    c.create_arc(x2 - 2 * r, y2 - 2 * r, x2, y2, start=270, extent=90, fill=fill, outline=fill, width=0)


def blend_colors(a: str, b: str, t: float) -> str:
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

#The Main class that handles the UI theme, state and rendering
class CofferdamApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CofferdamCalc")
        self.root.geometry("1150x700")
        self.root.minsize(1050, 650)

        self.theme_name = tk.StringVar(value="light")
        self.selected_sheet = tk.StringVar(value="")
        self.selected_waler = tk.StringVar(value="")
        self.current = tk.StringVar(value="sheet")

        self.active_card = None
        self.labels = []
        self.desc_labels = []
        self.grad_buttons = []

        self.build_layout()
        self.render_sheet()
        self.root.mainloop()

    #Gives teh current theme that is selected
    @property
    def theme(self):
        return THEMES[self.theme_name.get()]
    #Builds both the static layout portions (the top bar and screen container)
    def build_layout(self):
        self.topbar = tk.Frame(self.root, height=60, bg=self.theme["page_bg"])
        self.topbar.pack(fill=tk.X)

        self.toggle_canvas = tk.Canvas(
            self.topbar, width=140, height=36, bd=0, highlightthickness=0, cursor="hand2"
        )
        self.toggle_canvas.pack(side=tk.RIGHT, padx=20, pady=12)
        self.toggle_canvas.bind("<Button-1>", lambda e: self.toggle_theme())

        self.screen = tk.Frame(self.root, bg=self.theme["page_bg"])
        self.screen.pack(fill=tk.BOTH, expand=True)

        self.draw_toggle()

    def draw_toggle(self):
        self.toggle_canvas.delete("all")
        self.toggle_canvas.configure(bg=self.theme["page_bg"])
        rounded_rect(self.toggle_canvas, 0, 0, 140, 36, 8, fill="#FFFFFF", outline="#CCCCCC")
        label = "🌙 Dark Mode" if self.theme_name.get() == "light" else "☀ Light Mode"
        self.toggle_canvas.create_text(
            70, 18, text=label, fill="#1F2937", font=("Arial", 10, "bold")
        )

    def toggle_theme(self):
        self.theme_name.set("dark" if self.theme_name.get() == "light" else "light")
        self.render()

    def clear_screen(self):
        for w in self.screen.winfo_children():
            w.destroy()
        self.active_card = None
        self.labels.clear()
        self.desc_labels.clear()
        self.grad_buttons.clear()

    def make_card(self):
        card = tk.Frame(
            self.screen,
            bg=self.theme["card_bg"],
            highlightthickness=1,
            highlightbackground=self.theme["card_border"],
        )
        card.place(relx=0.5, rely=0.5, anchor="center", width=980, height=560)
        self.active_card = card
        return card

    def apply_theme(self):
        self.root.configure(bg=self.theme["page_bg"])
        self.topbar.configure(bg=self.theme["page_bg"])
        self.screen.configure(bg=self.theme["page_bg"])
        self.draw_toggle()

        if self.active_card:
            self.active_card.configure(
                bg=self.theme["card_bg"],
                highlightbackground=self.theme["card_border"],
            )

        for lbl, kind in self.labels:
            lbl.configure(
                bg=self.theme["card_bg"],
                fg=self.theme["text"] if kind == "text" else self.theme["muted"],
            )

        for lbl in self.desc_labels:
            lbl.configure(bg=self.theme["card_bg"], fg=self.theme["muted"])

        for gb in self.grad_buttons:
            gb.redraw()

    def render(self):
        if self.current.get() == "sheet":
            self.render_sheet()
        else:
            self.render_waler()
    #renders the selection screen for the user
    def render_sheet(self):
        self.clear_screen()
        self.current.set("sheet")
        card = self.make_card()

        title = tk.Label(
            card,
            text="Cofferdam Sheet Pile Analysis",
            font=("Arial", 26),
            bg=self.theme["card_bg"],
            fg=self.theme["text"],
        )
        title.pack(pady=(20, 22))
        self.labels.append((title, "text"))

        grid = tk.Frame(card, bg=self.theme["card_bg"])
        grid.pack(fill=tk.BOTH, expand=True, padx=30)

        keys = list(SHEET_PILE_CASES.keys())
        left_col = keys[0::2]
        right_col = keys[1::2]

        def case_block(parent, case_name, r, c):
            cell = tk.Frame(parent, bg=self.theme["card_bg"])
            cell.grid(row=r, column=c, padx=18, pady=6, sticky="nsew")

            gb = GradientButton(
                cell,
                text=case_name,
                command=lambda n=case_name: self.select_sheet_case(n),
                theme_getter=lambda: self.theme,
                width=360,
                height=52,
                radius=26,
                selected=(self.selected_sheet.get() == case_name),
            )
            gb.pack(pady=(0, 4))
            self.grad_buttons.append(gb)

            d = tk.Label(
                cell,
                text=SHEET_PILE_CASES[case_name],
                font=("Arial", 10),
                wraplength=380,
                justify="center",
                bg=self.theme["card_bg"],
                fg=self.theme["muted"],
            )
            d.pack()
            self.desc_labels.append(d)

        for r in range(3):
            case_block(grid, left_col[r], r, 0)
            case_block(grid, right_col[r], r, 1)

        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)
        for r in range(3):
            grid.grid_rowconfigure(r, weight=1)

        footer = tk.Frame(card, bg=self.theme["card_bg"])
        footer.pack(fill=tk.X, pady=(10, 16), padx=30)

        status = tk.Label(
            footer,
            text=f"Selected: {self.selected_sheet.get() or '(none)'}",
            font=("Arial", 11, "bold"),
            bg=self.theme["card_bg"],
            fg=self.theme["text"],
        )
        status.pack(side=tk.LEFT)
        self.labels.append((status, "text"))

        next_btn = GradientButton(
            footer,
            text="Next →",
            command=self.render_waler,
            theme_getter=lambda: self.theme,
            width=200,
            height=46,
            radius=23,
        )
        next_btn.pack(side=tk.RIGHT)
        next_btn.set_disabled(not bool(self.selected_sheet.get()))
        self.grad_buttons.append(next_btn)

        self.apply_theme()

    def select_sheet_case(self, name):
        self.selected_sheet.set(name)
        self.selected_waler.set("")
        self.render()

    def render_waler(self):
        if not self.selected_sheet.get():
            return

        self.clear_screen()
        self.current.set("waler")
        card = self.make_card()

        title = tk.Label(
            card,
            text="Select Waler Case",
            font=("Arial", 24, "bold"),
            bg=self.theme["card_bg"],
            fg=self.theme["text"],
        )
        title.pack(pady=(26, 8))
        self.labels.append((title, "text"))

        sub = tk.Label(
            card,
            text=f"Sheet Pile Case: {self.selected_sheet.get()}",
            font=("Arial", 12),
            bg=self.theme["card_bg"],
            fg=self.theme["muted"],
        )
        sub.pack(pady=(0, 22))
        self.labels.append((sub, "muted"))

        area = tk.Frame(card, bg=self.theme["card_bg"])
        area.pack(fill=tk.X, padx=70)

        for w_name in WALER_CASES:
            row = tk.Frame(area, bg=self.theme["card_bg"])
            row.pack(fill=tk.X, pady=12)

            gb = GradientButton(
                row,
                text=w_name,
                command=lambda n=w_name: self.select_waler_case(n),
                theme_getter=lambda: self.theme,
                width=820,
                height=52,
                radius=26,
                selected=(self.selected_waler.get() == w_name),
            )
            gb.pack(pady=(0, 6))
            self.grad_buttons.append(gb)

            d = tk.Label(
                row,
                text=WALER_CASES[w_name],
                font=("Arial", 10),
                bg=self.theme["card_bg"],
                fg=self.theme["muted"],
            )
            d.pack()
            self.desc_labels.append(d)

        footer = tk.Frame(card, bg=self.theme["card_bg"])
        footer.pack(fill=tk.X, pady=(18, 16), padx=70)

        back_btn = GradientButton(
            footer,
            text="← Back",
            command=self.render_sheet,
            theme_getter=lambda: self.theme,
            width=200,
            height=46,
            radius=23,
        )
        back_btn.pack(side=tk.LEFT)
        self.grad_buttons.append(back_btn)

        cont_btn = GradientButton(
            footer,
            text="Continue →",
            command=lambda: messagebox.showinfo(
                "Selection Confirmed",
                f"Sheet Pile: {self.selected_sheet.get()}\nWaler: {self.selected_waler.get()}",
            ),
            theme_getter=lambda: self.theme,
            width=220,
            height=46,
            radius=23,
        )
        cont_btn.pack(side=tk.RIGHT)
        cont_btn.set_disabled(not bool(self.selected_waler.get()))
        self.grad_buttons.append(cont_btn)

        self.apply_theme()

    def select_waler_case(self, name):
        self.selected_waler.set(name)
        self.render()


if __name__ == "__main__":
    CofferdamApp()
