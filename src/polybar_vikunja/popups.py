from .config_helper import PolybarVikunjaConfig
from tkinter import *


class ConfigPopup():

    def __init__(self, lists=None):
        self.root = Tk(className="polybar-vikunja")
        self.root.attributes('-type', 'dialog')
        self.config = PolybarVikunjaConfig()

        self.position_window()


        lists = [
            {
                "title": e["title"],
                "id": e["id"]
            } for e in lists
        ]

        listbox = Listbox(
            self.root,
            selectmode='SINGLE',
        )

        selected_index = None
        for i in range(len(lists)):
            e = lists[i]
            listbox.insert(e["id"], e["title"])

            if str(e["id"]) == self.config.get("default_list", None):
                selected_index = i

        listbox.selection_set(selected_index)
        listbox.see(selected_index)

        scrollbar = Scrollbar(self.root)
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        def handle_list_select(event):
            selected_index = listbox.curselection()[0]
            self.config.set(
                "default_list",
                str(lists[selected_index]["id"])
            )

        listbox.bind("<<ListboxSelect>>", handle_list_select)
        listbox.grid(row=0, column=0)

        self.attach_close_window_handler()
        self.root.mainloop()

    def position_window(self):
        width = 250
        height = 250

        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        abs_coord_x = self.root.winfo_pointerx() - self.root.winfo_vrootx()
        abs_coord_y = self.root.winfo_pointery() - self.root.winfo_vrooty()

        abs_coord_x -= int(width / 2)
        abs_coord_y -= int(height) - int(height / 10)

        self.root.geometry(f"{width}x{height}+{abs_coord_x}+{abs_coord_y}")

    def attach_close_window_handler(self):
        def close_window(event=None):
            self.root.destroy()
        self.root.bind("<FocusOut>", close_window)
