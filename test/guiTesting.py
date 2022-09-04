"""Source: https://github.com/rdbende/ttk-widget-factory"""

import tkinter as tk
from tkinter import ttk

import sv_ttk


class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        # Make the app responsive
        for index in (0, 1, 2):
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        # Create value lists
        self.option_menu_list = ["", "OptionMenu", "Option 1", "Option 2"]
        self.combo_list = ["Combobox", "Editable item 1", "Editable item 2"]
        self.readonly_combo_list = ["Readonly combobox", "Item 1", "Item 2"]

        # Create control variables
        self.var_0 = tk.BooleanVar()
        self.var_1 = tk.BooleanVar(value=True)
        self.var_2 = tk.BooleanVar()
        self.var_3 = tk.IntVar(value=2)
        self.var_4 = tk.StringVar(value=self.option_menu_list[1])
        self.var_5 = tk.DoubleVar(value=75.0)

        # Create widgets
        self.setup_widgets()

    def setup_widgets(self):
        # Panedwindow
        self.paned = ttk.PanedWindow(self)
        self.paned.grid(row=0, column=2, pady=(25, 5), sticky="nsew", rowspan=3)

        # Pane #1
        self.pane_1 = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane_1, weight=1)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.pane_1)
        self.scrollbar.pack(side="right", fill="y")

        # Treeview
        self.treeview = ttk.Treeview(
            self.pane_1,
            columns=("1", "2"),
            height=10,
            selectmode="browse",
            show=("tree",),
            yscrollcommand=self.scrollbar.set,
        )
        self.treeview.pack(expand=True, fill="both")
        self.scrollbar.config(command=self.treeview.yview)

        # Treeview columns
        self.treeview.column("#0", anchor="w", width=120)
        self.treeview.column(1, anchor="w", width=120)
        self.treeview.column(2, anchor="w", width=120)

        # Define treeview data
        treeview_data = [
            ("", 1, "Parent", (" ", " ")),
            (1, 2, "Sub-parent", ("Subitem 2.2", "Value 2.2")),
            (2, 3, "Child", ("Subitem 2.2.1", "Value 2.2.1")),
            (2, 4, "Child", ("Subitem 2.2.2", "Value 2.2.2")),
            (2, 5, "Child", ("Subitem 2.2.3", "Value 2.2.3")),
            (1, 6, "Sub-parent", ("Subitem 2.2", "Value 2.2")),
            (6, 7, "Child", ("Subitem 2.4", "Value 2.4")),
            (6, 8, "Child", ("Subitem 2.4", "Value 2.4")),
            (6, 9, "Child", ("Subitem 2.4", "Value 2.4")),
            (6, 10, "Child", ("Subitem 2.4", "Value 2.4")),

        ]

        # Insert treeview data
        for item in treeview_data:
            parent, iid, text, values = item
            self.treeview.insert(
                parent=parent, index="end", iid=iid, text=text, values=values
            )

            if not parent or iid in {8, 21}:
                self.treeview.item(iid, open=True)  # Open parents

        # Select and scroll
        self.treeview.selection_set("10")
        self.treeview.see("7")
def main():
    root = tk.Tk()
    root.title("Simple example")

    sv_ttk.set_theme("dark")

    app = App(root)
    app.pack(fill="both", expand=True)

    root.update_idletasks()  # Make sure every screen redrawing is done

    width, height = root.winfo_width(), root.winfo_height()
    x = int((root.winfo_screenwidth() / 2) - (width / 2))
    y = int((root.winfo_screenheight() / 2) - (height / 2))

    # Set a minsize for the window, and place it in the middle
    root.minsize(width, height)
    root.geometry(f"+{x}+{y}")

    root.mainloop()
if __name__ == "__main__":
    main()