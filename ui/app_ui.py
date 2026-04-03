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

02/27/2026
Author: Adetola Aladekoba

Updated main.py to align with the new class-based UI architecture after the transition from a function-based run_app structure to 
the CofferdamApp class. Resolved an ImportError caused by main.py attempting to import a removed run_app function. 
Modified the entry point to correctly instantiate and launch the CofferdamApp class. Verified successful execution from the terminal
using python3 main.py. Additionally reviewed the project folder structure to maintain modular separation between UI, calculations, and core application files.

03/01/2026
Author: Rylan Weldon
Added clarrifying comments to several portions of the code

05/03/2026
Author: Rylan Weldon
Added the seventh case to the UI. Made it so that the waler screen would only show when case seven was selected. Imported the cofferedam library
and added input screens for all seven cases. Added calculations for all of the cases. Reformed the sized of the window and card to match inputs.
"""

import tkinter as tk
from tkinter import messagebox
import CofferdamLibrary

SHEET_PILE_CASES = {
    "Case 1": "Determine cantilever moment when cofferdam is excavated to install top waler",
    "Case 2": "Determine wall moment and top waler loading after excavation",
    "Case 3": "Determine wall moment and top waler loading after excavation with water on the outside of the wall with two additional walers",
    "Case 4": "Determine wall moments and waler loadings for two or more walers",
    "Case 5": "Determine case five configuration",
    "Case 6": "Determine moment and minimum length of sheetpile for a cantilevered bulkhead",
    "Case 7": "Determine the combined stresses for different shaped cofferdam walers",
}

WALER_CASES = {
    "Waler I": "Waler for full circle",
    "Waler II": "Waler for semi-circle",
    "Waler III": "Waler for segmental arch",
}

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
        self.root.minsize(1050, 800)

        self.theme_name = tk.StringVar(value="light")
        self.selected_sheet = tk.StringVar(value="")
        self.selected_waler = tk.StringVar(value="")
        self.current = tk.StringVar(value="sheet")

        self.active_card = None
        self.labels = []
        self.desc_labels = []
        self.grad_buttons = []
        self.input_entries = {}
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
        self.input_entries.clear()

    def make_card(self):
        card = tk.Frame(
            self.screen,
            bg=self.theme["card_bg"],
            highlightthickness=1,
            highlightbackground=self.theme["card_border"],
        )
        card.place(relx=0.5, rely=0.5, anchor="center", width=1110, height=750)
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
        for name, ent in self.input_entries.items(): 
            ent.configure(bg=self.theme["page_bg"], fg=self.theme["text"], insertbackground=self.theme["text"])        
        for gb in self.grad_buttons:
            gb.redraw()

    def render(self):
        if self.current.get() == "sheet":
            self.render_sheet()
        elif self.current.get() == "waler":
            self.render_waler()
        else: 
            self.render_inputs() 
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
        numberOfRows = (len(keys)+1)
        for r in range(numberOfRows):
            if r < len(left_col):
                case_block(grid, left_col[r], r, 0)
            if r < len(right_col):
                case_block(grid, right_col[r], r, 1)

        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)
        for r in range(numberOfRows):
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
            #for the odd case
            command=lambda: self.render_waler() if self.selected_sheet.get() == "Case 7" else self.render_inputs(),
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
            command=self.render_inputs,
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
    def render_inputs(self):
        self.clear_screen()
        self.current.set("inputs")
        card = self.make_card()
        sheet = self.selected_sheet.get()
        waler = self.selected_waler.get()

        header_text = f"Parameters for {sheet}" + (f" - {waler}" if waler else "")
        title = tk.Label(card, text=header_text, font=("Arial", 22, "bold"), bg=self.theme["card_bg"], fg=self.theme["text"])
        title.pack(pady=(20, 10))
        self.labels.append((title, "text"))

        form_area = tk.Frame(card, bg=self.theme["card_bg"])
        form_area.pack(fill=tk.BOTH, expand=True, padx=120)
        fields = []
        if sheet == "Case 1": fields = ["S", "L", "PA", "PP"]
        elif sheet == "Case 2": fields = ["S", "L", "PA", "PP", "D"]
        elif sheet == "Case 3": fields = ["S", "L", "PA", "PP", "D", "DW"]
        elif sheet == "Case 4": fields = ["S", "L", "PA", "PP", "D", "DW", "L1", "L2", "L3", "L4", "L5", "L6"]
        elif sheet == "Case 5": fields = ["S", "PA", "PP", "D"]
        elif sheet == "Case 6": fields = ["S", "PA", "PP", "D", "DW"]
        elif sheet == "Case 7":
            if waler == "Waler I": fields = ["R", "W", "E", "S", "H", "FC", "FY", "rebarList"]
            elif waler == "Waler II": fields = ["R", "W", "S", "H", "FC", "FY", "rebarList"]
            elif waler == "Waler III": fields = ["R", "W", "T", "C", "S", "H", "FC", "FY", "rebarList"]

        #after inputs are confirmed, remove
        if not fields:
            lbl = tk.Label(form_area, text="Inputs not yet defined for this case.", font=("Arial", 12), bg=self.theme["card_bg"], fg=self.theme["muted"])
            lbl.pack(pady=40)
            self.labels.append((lbl, "muted"))
        else:
            for f in fields:
                row = tk.Frame(form_area, bg=self.theme["card_bg"])
                row.pack(fill=tk.X, pady=8)
                label_text = f + (" (Qty, Size e.g., '2,8')" if f == "rebarList" else "") + ":"
                lbl = tk.Label(row, text=label_text, width=25, anchor="e", font=("Arial", 12), bg=self.theme["card_bg"], fg=self.theme["text"])
                lbl.pack(side=tk.LEFT, padx=15)
                self.labels.append((lbl, "text"))
                ent = tk.Entry(row, font=("Arial", 12), bg=self.theme["page_bg"], fg=self.theme["text"], insertbackground=self.theme["text"], relief="flat", highlightthickness=1, highlightbackground=self.theme["card_border"])
                ent.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
                self.input_entries[f] = ent

        footer = tk.Frame(card, bg=self.theme["card_bg"])
        footer.pack(fill=tk.X, pady=(18, 16), padx=70)
        #
        back_command = self.render_sheet
        if sheet == "Case 7": 
            back_command = self.render_waler
        back_btn = GradientButton(footer, text="← Back", command=back_command, theme_getter=lambda: self.theme, width=200, height=46, radius=23)
        back_btn.pack(side=tk.LEFT)
        self.grad_buttons.append(back_btn)

        if fields:
            calc_btn = GradientButton(footer, text="Calculate →", command=self.execute_calc, theme_getter=lambda: self.theme, width=220, height=46, radius=23)
            calc_btn.pack(side=tk.RIGHT)
            self.grad_buttons.append(calc_btn)
        self.apply_theme()

    def execute_calc(self):
        try:
            kwargs = {}
            #for formatting the inputs for rebar list
            for field, entry in self.input_entries.items():
                val = entry.get().strip()
                if not val: raise ValueError(f"Field '{field}' cannot be empty.")
                if field == "rebarList":
                    parts = val.split(',')
                    if len(parts) != 2: raise ValueError("Rebar List must be in \"Qty,Size\" format (ex: 2,8).")
                    kwargs['rebarList'] = [(int(parts[0].strip()), int(parts[1].strip()))]
                else:
                    kwargs[field] = float(val)
                    
            sheet = self.selected_sheet.get()
            waler = self.selected_waler.get()
            res = {}

            if sheet == "Case 1": res = CofferdamLibrary.case1(kwargs['S'], kwargs['L'], kwargs['PA'], kwargs['PP'])
            elif sheet == "Case 2": res = CofferdamLibrary.case2(kwargs['S'], kwargs['L'], kwargs['PA'], kwargs['PP'], kwargs['D'])
            elif sheet == "Case 3": res = CofferdamLibrary.case3(kwargs['S'], kwargs['L'], kwargs['PA'], kwargs['PP'], kwargs['D'], kwargs['DW'])
            elif sheet == "Case 4": res = CofferdamLibrary.case4(kwargs['S'], kwargs['L'], kwargs['PA'], kwargs['PP'], kwargs['D'], kwargs['DW'], kwargs['L1'], kwargs['L2'], kwargs['L3'], kwargs['L4'], kwargs['L5'], kwargs['L6'])
            elif sheet == "Case 5": res = CofferdamLibrary.case5(kwargs['S'], kwargs['PA'], kwargs['PP'], kwargs['D'])
            elif sheet == "Case 6": res = CofferdamLibrary.case6(kwargs['S'], kwargs['PA'], kwargs['PP'], kwargs['D'], kwargs['DW'])
            elif sheet == "Case 7":
                if waler == "Waler I": res = CofferdamLibrary.case7c1(kwargs['R'], kwargs['W'], kwargs['E'], kwargs['S'], kwargs['H'], kwargs['FC'], kwargs['FY'], kwargs['rebarList'])
                elif waler == "Waler II": res = CofferdamLibrary.case7c2(kwargs['R'], kwargs['W'], kwargs['S'], kwargs['H'], kwargs['FC'], kwargs['FY'], kwargs['rebarList'])
                elif waler == "Waler III": res = CofferdamLibrary.case7c3(kwargs['R'], kwargs['W'], kwargs['T'], kwargs['C'], kwargs['S'], kwargs['H'], kwargs['FC'], kwargs['FY'], kwargs['rebarList'])

            result_str = "\n".join([f"{k}: {round(v, 4) if isinstance(v, float) else v}" for k, v in res.items()])
            messagebox.showinfo(f"{sheet} Results", result_str)

        except Exception as e:
            messagebox.showerror("Calculation Error", f"An error occurred: {e}")    
if __name__ == "__main__":
    CofferdamApp()
