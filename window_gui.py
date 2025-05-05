import math
import tkinter as tk
from tkinter import PhotoImage
from PIL import ImageTk, Image
import os
import subprocess

class DesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to IR's Window GUI")
        self.root.geometry("400x300")

        self.original_bg = Image.open("IMAGES/IR x ST.png")
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        dummy_img = ImageTk.PhotoImage(Image.new("RGB", (1, 1)))
        self.bg_item = self.canvas.create_image(0, 0, anchor="nw", image=dummy_img)
        self.canvas.image = dummy_img

        self.root.bind("<Configure>", self.resize_bg)
        self.root.after(100, self.resize_bg)

        self.btns = ["Introduction", "About", "Contact", "GTN-IR", "Exit"]
        img_paths = [
            "IMAGES/Information icon.png",
            "IMAGES/About icon.png",
            "IMAGES/Contact icon.png",
            "IMAGES/GTN-IR.png",
            "IMAGES/Exit icon.png"
        ]

        self.original_imgs = [Image.open(p) for p in img_paths]
        self.imgs = [ImageTk.PhotoImage(img.resize((50, 50))) for img in self.original_imgs]

        self.hovering = {}
        self.button_list = []

        self.create_buttons()

        # --- Taskbar ---
        self.taskbar = tk.Frame(self.root, bg="gray20", height=30)
        self.taskbar.pack(side="bottom", fill="x")

        self.start_btn = tk.Button(self.taskbar, text="Start", bg="gray30", fg="white", relief="flat", command=self.toggle_start_menu)
        self.start_btn.pack(side="left", padx=5)

        self.clock_label = tk.Label(self.taskbar, fg="white", bg="gray20")
        self.clock_label.pack(side="right", padx=10)
        self.update_clock()

        # --- Start Menu Popup ---
        self.start_menu = tk.Frame(self.root, bg="gray30", bd=2, relief="raised")
        self.start_menu_visible = False

        self.app_dock = tk.Frame(self.root, bg="gray15", width=50)
        self.app_dock.pack(side="left", fill="y")

        # Dictionary to track opened windows
        self.opened_apps = {}
        self.dock_icons = {}


    def toggle_start_menu(self):
        if self.start_menu_visible:
            self.start_menu.place_forget()
            self.start_menu_visible = False
        else:
            self.start_menu.place(x=0, y=self.root.winfo_height() - 130)  # Adjust height for your layout
            self.populate_start_menu()
            self.start_menu_visible = True

    def populate_start_menu(self):
        for widget in self.start_menu.winfo_children():
            widget.destroy()

        tk.Button(self.start_menu, text="Notepad", width=20, command=lambda: self.open_notepad("intro")).pack(pady=2)
        tk.Button(self.start_menu, text="Settings", width=20, command=self.show_settings).pack(pady=2)
        tk.Button(self.start_menu, text="Exit", width=20, command=self.root.quit).pack(pady=2)

    def show_settings(self):
        settings_win = tk.Toplevel(self.root)
        settings_win.title("Settings")
        settings_win.geometry("300x200")
        tk.Label(settings_win, text="Settings Placeholder").pack(pady=20)

    def update_clock(self):
        import time
        current_time = time.strftime("%H:%M:%S")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)


    def on_start(self):
        print("Start button clicked!")
        # You could open a new menu or simulate a start menu here

    def update_clock(self):
        import time
        current_time = time.strftime("%H:%M:%S")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)

    def resize_bg(self, event=None):
        new_w = self.root.winfo_width()
        new_h = self.root.winfo_height()
        resized = self.original_bg.resize((new_w, new_h), Image.LANCZOS)
        new_bg = ImageTk.PhotoImage(resized)
        self.canvas.itemconfig(self.bg_item, image=new_bg)
        self.canvas.image = new_bg

    def create_buttons(self):
        total = len(self.btns)
        cols = min(5, total)  # Set a max per row
        rows = math.ceil(total / cols)

        padding_x = 150
        padding_y = 150
        start_x = 100
        start_y = 100

        for idx, label in enumerate(self.btns):
            row = idx // cols
            col = idx % cols

            b = tk.Button(
                self.canvas,
                text=label,
                image=self.imgs[idx],
                compound="top",
                command=lambda n=label: self.on_click(n)
            )

            x = start_x + col * padding_x
            y = start_y + row * padding_y

            self.canvas.create_window(x, y, window=b)
            b.bind("<Enter>", lambda e, i=idx: self.on_enter(e, i))
            b.bind("<Leave>", lambda e, i=idx: self.on_leave(e, i))
            self.button_list.append((b, idx))



    def on_click(self, name):
        mapping = {
            "Introduction": "intro",
            "About": "about",
            "Contact": "contact",
            "Exit": "exit",
            "GTN-IR": "gtn-ir"
        }
        self.open_notepad(mapping.get(name))

    def open_notepad(self, on):
        if on == "exit":
            self.root.quit()
            return

        if on == "gtn-ir":
            game_path = "F:/Python/4. Number Guessing Game/4. Number Guessing Game.py"
            game_dir = os.path.dirname(game_path)
            subprocess.Popen(["python", game_path], cwd=game_dir)
            return

        if on in self.opened_apps:
            self.opened_apps[on].lift()
            return

        nwd = tk.Toplevel(self.root)
        nwd.geometry("600x500")
        nwd.config(bg="Yellow")
        self.opened_apps[on] = nwd

        def on_close():
            nwd.destroy()
            self.opened_apps.pop(on, None)
            self.remove_from_dock(on)

        nwd.protocol("WM_DELETE_WINDOW", on_close)

        # Add to dock
        self.add_to_dock(on, nwd)

        frame = tk.Frame(nwd)
        frame.pack(fill="both", expand=True)

        txt = tk.Text(frame, wrap="word", font=("Consolas", 12))
        scrollbar = tk.Scrollbar(frame, command=txt.yview)
        txt.config(yscrollcommand=scrollbar.set)

        content = self.get_text_content(on)
        nwd.title(f"IR.{on.capitalize()}")
        txt.insert(tk.END, content)
        txt.config(state="disabled")

        txt.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

    def add_to_dock(self, name, window):
        if name in self.dock_icons:
            return

        icon_map = {
            "intro": "IMAGES/Information icon.png",
            "about": "IMAGES/About icon.png",
            "contact": "IMAGES/Contact icon.png",
            "gtn-ir": "IMAGES/GTN-IR.png",
            "exit": "IMAGES/Exit icon.png"
        }

        path = icon_map.get(name)
        if not path or not os.path.exists(path):
            return

        img = ImageTk.PhotoImage(Image.open(path).resize((30, 30)))
        btn = tk.Button(self.app_dock, image=img, command=window.lift, bg="gray15", relief="flat")
        btn.image = img
        btn.pack(pady=5)
        self.dock_icons[name] = btn

    def remove_from_dock(self, name):
        if name in self.dock_icons:
            self.dock_icons[name].destroy()
            del self.dock_icons[name]


    def get_text_content(self, key):
        texts = {
            "intro": """
Welcome to the Window-Style GUI!

This project is a simple simulation of a Windows desktop environment,
built entirely using Python and Tkinter.

Features:
- Icon-based buttons arranged in a grid layout.
- Cool button hover and click effects.
- Separate windows open with detailed information.
- Custom notepad-like text areas for a smooth user experience.

Developer:
- Name: Ishaan Ray
- Passionate about Python, GUI development, and learning new technologies!

Purpose:
This project is designed as a beginner-friendly hands-on exercise
to understand GUI building blocks like windows, buttons, events,
layouts, and text areas in Python.

Thank you for checking out this project! 🎉""",
            "about": """
About This Application

This project showcases a beginner-friendly, desktop-like GUI environment
using Python and the Tkinter library.

Key Highlights:
- Icon-based clickable buttons that simulate desktop shortcuts.
- Dynamic window opening with text-based content.
- Organized grid layout, smooth interface, and responsive design.
- Simple yet expandable framework for bigger projects.

Technologies Used:
- Python 3
- Tkinter (for GUI components)

Inspiration:
The design is inspired by classic Windows desktops,
providing a familiar and easy-to-navigate experience for users.

Goals:
- To practice Python GUI development.
- To learn window management, event handling, and layouts.
- To create a user-friendly and visually appealing project.

Keep exploring and building! 🚀""",
            "contact": """
Contact Us

We would love to hear from you!

For any inquiries, feedback, suggestions, or collaboration opportunities,
please feel free to reach out through the following channels:

Email:
ishaanray.cs.19@gmail.com

Phone:
+91 98792 97676

You can also connect with us for updates, new projects, and learning resources!

Thank you for using this application. 
We appreciate your support and encouragement! 🚀"""
        }
        return texts.get(key, "")

    def animate_resize(self, widget, idx, grow=True, step=0):
        if not self.hovering.get(widget, False) and grow:
            return
        if self.hovering.get(widget, False) and not grow:
            return

        base_size = 50
        max_size = 55
        size_step = 2

        new_size = base_size + step * size_step if grow else max_size - step * size_step
        new_size = max(min(new_size, max_size), base_size)

        resized_img = self.original_imgs[idx].resize((new_size, new_size), Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(resized_img)
        widget.config(image=tk_img)
        widget.image = tk_img

        if (grow and new_size < max_size) or (not grow and new_size > base_size):
            widget.after(30, self.animate_resize, widget, idx, grow, step + 1)

    def on_enter(self, event, idx):
        self.hovering[event.widget] = True
        event.widget.config(bg="lightblue")
        self.animate_resize(event.widget, idx, grow=True)

    def on_leave(self, event, idx):
        self.hovering[event.widget] = False
        event.widget.config(bg="SystemButtonFace")
        self.animate_resize(event.widget, idx, grow=False)

if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopApp(root)
    root.mainloop()