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

04/03/2026
Author: Rylan Weldon
Added the seventh case to the UI. Made it so that the waler screen would only show when case seven was selected. Imported the cofferedam library
and added input screens for all seven cases. Added calculations for all of the cases. Reformed the sized of the window and card to match inputs.

04/10/2026
Author: Rylan Weldon
Added visualizations for case 1, 2, 3, 5,  7(subcases I, II, III). The visualizations vary by case. Also reformated the outputs screen to showcase the outputs
alongside the visualization information, accomponied with a back button. 
"""
import tkinter as tk
from tkinter import messagebox
import CofferdamLibrary
import matplotlib.pyplot as plt 
from matplotlib.patches import Rectangle, Circle 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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

        for labelText, kind in self.labels:
            labelText.configure(
                bg=self.theme["card_bg"],
                fg=self.theme["text"] if kind == "text" else self.theme["muted"],
            )

        for labelText in self.desc_labels:
            labelText.configure(bg=self.theme["card_bg"], fg=self.theme["muted"])
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
        #for cleaning the screen
        self.clear_screen()
        self.current.set("waler")
        card = self.make_card()

        title = tk.Label(
            card,
            text="Select Waler Case",
            font=("Arial", 23, "bold"),
            bg=self.theme["card_bg"],
            fg=self.theme["text"],
        )
        title.pack(pady=(26, 8))
        self.labels.append((title, "text"))

        sub = tk.Label(
            card,
            text="Sheet Pile Case: "+self.selected_sheet.get(),
            font=("Arial", 11),
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
        footer.pack(fill=tk.X, pady=(18, 17), padx=69)

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

        if waler:
            headerText = "Results for "+sheet+" - "+waler+""
        else:
            headerText = "Results for "+sheet+""
        title = tk.Label(card, text=headerText, font=("Arial", 21, "bold"), bg=self.theme["card_bg"], fg=self.theme["text"])
        title.pack(pady=(20, 10))
        self.labels.append((title, "text"))

        form_area = tk.Frame(card, bg=self.theme["card_bg"])
        form_area.pack(fill=tk.BOTH, expand=True, padx=120)
        fields = []
        if sheet == "Case 1": 
            fields = ["S", "L", "PA", "PP"]
        elif sheet == "Case 2": 
            fields = ["S", "L", "PA", "PP", "D"]
        elif sheet == "Case 3": 
            fields = ["S", "L", "PA", "PP", "D", "DW"]
        elif sheet == "Case 4": 
            fields = ["S", "L", "PA", "PP", "D", "DW", "L1", "L2", "L3", "L4", "L5", "L6"]
        elif sheet == "Case 5": 
            fields = ["S", "PA", "PP", "D"]
        elif sheet == "Case 6": 
            fields = ["S", "PA", "PP", "D", "DW"]
        elif sheet == "Case 7":
            if waler == "Waler I": 
                fields = ["R", "W", "E", "S", "H", "FC", "FY", "rebarList"]
            elif waler == "Waler II": 
                fields = ["R", "W", "S", "H", "FC", "FY", "rebarList"]
            elif waler == "Waler III": 
                fields = ["R", "W", "T", "C", "S", "H", "FC", "FY", "rebarList"]

        #after inputs are confirmed, remove
        if not fields:
            labelText = tk.Label(form_area, text="Inputs are not defined for case.", font=("Arial", 12), bg=self.theme["card_bg"], fg=self.theme["muted"])
            labelText.pack(pady=40)
            self.labels.append((labelText, "muted"))
        else:
            for f in fields:
                #for thhe field mapping
                row = tk.Frame(form_area, bg=self.theme["card_bg"])
                row.pack(fill=tk.X, pady=8)
                label_text = f + (" (Qty, Size e.g., '2,8')" if f == "rebarList" else "") + ":"
                labelText = tk.Label(row, text=label_text, width=25, anchor="e", font=("Arial", 12), bg=self.theme["card_bg"], fg=self.theme["text"])
                labelText.pack(side=tk.LEFT, padx=15)
                self.labels.append((labelText, "text"))
                ent = tk.Entry(row, font=("Arial", 12), bg=self.theme["page_bg"], fg=self.theme["text"], insertbackground=self.theme["text"], relief="flat", highlightthickness=1, highlightbackground=self.theme["card_border"])
                ent.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
                self.input_entries[f] = ent

        footer = tk.Frame(card, bg=self.theme["card_bg"])
        footer.pack(fill=tk.X, pady=(18, 17), padx=69)
        
        backButton = self.render_sheet
        if sheet == "Case 7": 
            backButton = self.render_waler
        back_btn = GradientButton(footer, text="← Back", command=backButton, theme_getter=lambda: self.theme, width=200, height=46, radius=23)
        back_btn.pack(side=tk.LEFT)
        self.grad_buttons.append(back_btn)

        if fields:
            caclculateButton = GradientButton(footer, text="Calculate →", command=self.execute_calc, theme_getter=lambda: self.theme, width=220, height=46, radius=23)
            caclculateButton.pack(side=tk.RIGHT)
            self.grad_buttons.append(caclculateButton)
        self.apply_theme()
    def render_results(self, sheet, waler, kwargs, res):
        self.clear_screen()
        self.current.set("results")
        card = self.make_card()
    
        if waler:
            headerText = "Results for "+sheet+" - "+waler+""
        else:
            headerText = "Results for "+sheet+""
        title = tk.Label(card, text=headerText, font=("Arial", 21, "bold"), bg=self.theme["card_bg"], fg=self.theme["text"])
        title.pack(pady=(20, 10))
        self.labels.append((title, "text"))
    
        #creates the split for the results layout
        content_area = tk.Frame(card, bg=self.theme["card_bg"])
        content_area.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)
    
        left_frame = tk.Frame(content_area, bg=self.theme["card_bg"])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
        right_frame = tk.Frame(content_area, bg=self.theme["card_bg"])
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
        #for left side
        res_canvas = tk.Canvas(left_frame, bg=self.theme["card_bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(left_frame, orient="vertical", command=res_canvas.yview)
        scrollable_frame = tk.Frame(res_canvas, bg=self.theme["card_bg"])
    
        scrollable_frame.bind("<Configure>", lambda e: res_canvas.configure(scrollregion=res_canvas.bbox("all")))
        res_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        res_canvas.configure(yscrollcommand=scrollbar.set)
    
        res_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
        for k, v in res.items():
            if k in ["Moments", "YValues"]: 
                continue
            val_str = str(round(v, 4)) if isinstance(v, float) else str(v)
            row = tk.Frame(scrollable_frame, bg=self.theme["card_bg"])
            row.pack(fill=tk.X, pady=4, anchor="w")
            labelText_key = tk.Label(row, text=f"{k}:", font=("Arial", 12, "bold"), bg=self.theme["card_bg"], fg=self.theme["muted"], width=8, anchor="w")
            labelText_key.pack(side=tk.LEFT)
            labelText_val = tk.Label(row, text=val_str, font=("Arial", 12), bg=self.theme["card_bg"], fg=self.theme["text"])
            labelText_val.pack(side=tk.LEFT)
            self.labels.extend([(labelText_key, "muted"), (labelText_val, "text")])
    
        #right side for making the figure
        fig = plt.figure(figsize=(5, 5))
        hasPlot = False
    
        if sheet == "Case 1":
            bars = ['P1 (Surcharge)', 'P2 (Active)', 'P3 (Cross)', 'P4 (Passive)']
            vals = [res.get('P1', 0), res.get('P2', 0), res.get('P3', 0), -res.get('P4', 0)]
            plt.barh(bars, vals, color=['#E74C3C', '#E74C3C', '#E74C3C', '#3498DB'])
            plt.axvline(0, color='black', linewidth=1.5)
            plt.title("Resultant Force Vectors")
            plt.xlabel("Force Magnitude (lbs/ft)")
            plt.grid(axis='x', linestyle='--', alpha=0.7)
            plt.tight_layout()
            hasPlot = True
    
        elif sheet in ["Case 2", "Case 3"]:
            if 'YValues' in res and 'Moments' in res and len(res['YValues']) > 0:
                plt.plot(res['Moments'], res['YValues'], color='#2C3E50', linewidth=2.5)
                plt.gca().invert_yaxis()
                plt.axvline(0, color='black', linewidth=1.5)
                plt.fill_betweenx(res['YValues'], res['Moments'], 0, alpha=0.3, color='#3498DB')
                plt.title(sheet+": Bending Moment Diagram")
                plt.ylabel("Depth")
                plt.xlabel("Bending Moment")
                plt.grid(True, linestyle='--', alpha=0.6)
                hasPlot = True
    
        elif sheet == "Case 5":
            forces = ['P1 (Sur.)', 'P2 (Act.)', 'P3 (M.)', 'VA (Ten.)', 'VC (Toe)']
            vals = [res.get('P1', 0), res.get('P2', 0), res.get('P3', 0), -res.get('VA', 0), -res.get('VC', 0)]
            plt.bar(forces, vals, color=['#E74C3C', '#E74C3C', '#E74C3C', '#2ECC71', '#3498DB'])
            plt.axhline(0, color='black', linewidth=1)
            plt.title("Loads vs Reactions")
            plt.ylabel("Force Magnitude")
            plt.xticks(rotation=15)
            plt.tight_layout()
            hasPlot = True
    
        elif sheet == "Case 7":
            ax = plt.gca()
            w_val, h_val = kwargs['S'], kwargs['H']
            rect = Rectangle((0, 0), w_val, h_val, fill=True, color='#BDC3C7', ec='black', lw=2)
            ax.add_patch(rect)
    
            qty, size = kwargs['rebarList'][0]
            spacing = w_val/(qty+1)
            rebarRadius = size/16
            for i in range(qty):
                circle = Circle(((i+1)*spacing,3),radius=rebarRadius,color='#2C3E50')
                ax.add_patch(circle)
    
            plt.xlim(-2, w_val + 2)
            plt.ylim(-2, h_val + 2)
            plt.gca().set_aspect('equal', adjustable='box')
            plt.title(f"Combined Stress Ratio: {res.get('CS', 0):.3f}")
            hasPlot = True
    
        if hasPlot:
            #SHOULD embed the plot into the results
            canvas = FigureCanvasTkAgg(fig, master=right_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        else:
            #will clean up if there isn't a plot
            plt.close(fig) 
            no_plot_labelText = tk.Label(right_frame, text="No visualization available for  calculation.", font=("Arial", 12, "italic"), bg=self.theme["card_bg"], fg=self.theme["muted"])
            no_plot_labelText.pack(expand=True)
            self.labels.append((no_plot_labelText, "muted"))
    
        #for the back button
        footer = tk.Frame(card, bg=self.theme["card_bg"])
        footer.pack(fill=tk.X, pady=(18, 16), padx=70)
    
        back_btn = GradientButton(footer, text="← Back to Inputs", command=self.render_inputs, theme_getter=lambda: self.theme, width=200, height=46, radius=23)
        back_btn.pack(side=tk.LEFT)
        self.grad_buttons.append(back_btn)
    
        self.apply_theme()    
    def execute_calc(self):
        try:
            kwargs = {}
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
    
            if sheet == "Case 1": 
                res = CofferdamLibrary.case1(kwargs['S'], kwargs['L'], kwargs['PA'], kwargs['PP'])
            elif sheet == "Case 2": 
                res = CofferdamLibrary.case2(kwargs['S'], kwargs['L'], kwargs['PA'], kwargs['PP'], kwargs['D'])
            elif sheet == "Case 3": 
                res = CofferdamLibrary.case3(kwargs['S'], kwargs['L'], kwargs['PA'], kwargs['PP'], kwargs['D'], kwargs['DW'])
            elif sheet == "Case 4": 
                res = CofferdamLibrary.case4(kwargs['S'], kwargs['L'], kwargs['PA'], kwargs['PP'], kwargs['D'], kwargs['DW'], kwargs['L1'], kwargs['L2'], kwargs['L3'], kwargs['L4'], kwargs['L5'], kwargs['L6'])
            elif sheet == "Case 5": 
                res = CofferdamLibrary.case5(kwargs['S'], kwargs['PA'], kwargs['PP'], kwargs['D'])
            elif sheet == "Case 6": 
                res = CofferdamLibrary.case6(kwargs['S'], kwargs['PA'], kwargs['PP'], kwargs['D'], kwargs['DW'])
            elif sheet == "Case 7":
                if waler == "Waler I": 
                    res = CofferdamLibrary.case7c1(kwargs['R'], kwargs['W'], kwargs['E'], kwargs['S'], kwargs['H'], kwargs['FC'], kwargs['FY'], kwargs['rebarList'])
                elif waler == "Waler II": 
                    res = CofferdamLibrary.case7c2(kwargs['R'], kwargs['W'], kwargs['S'], kwargs['H'], kwargs['FC'], kwargs['FY'], kwargs['rebarList'])
                elif waler == "Waler III": 
                    res = CofferdamLibrary.case7c3(kwargs['R'], kwargs['W'], kwargs['T'], kwargs['C'], kwargs['S'], kwargs['H'], kwargs['FC'], kwargs['FY'], kwargs['rebarList'])
    
            
            self.render_results(sheet, waler, kwargs, res)
    
        except Exception as e:
            messagebox.showerror("Calculation Error", "A error occurred: "+e)   
if __name__ == "__main__":
    CofferdamApp()
