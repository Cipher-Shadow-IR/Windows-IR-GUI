import tkinter as tk
from tkinter import PhotoImage
from PIL import ImageTk, Image


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

        self.btns = ["Introduction", "About", "Contact", "Exit"]
        img_paths = [
            "IMAGES/Information icon.png",
            "IMAGES/About icon.png",
            "IMAGES/Contact icon.png",
            "IMAGES/Exit icon.png",
        ]

        self.original_imgs = [Image.open(p) for p in img_paths]
        self.imgs = [ImageTk.PhotoImage(img.resize((50, 50))) for img in self.original_imgs]

        self.hovering = {}
        self.button_list = []

        self.create_buttons()

    def resize_bg(self, event=None):
        new_w = self.root.winfo_width()
        new_h = self.root.winfo_height()
        resized = self.original_bg.resize((new_w, new_h), Image.LANCZOS)
        new_bg = ImageTk.PhotoImage(resized)
        self.canvas.itemconfig(self.bg_item, image=new_bg)
        self.canvas.image = new_bg

    def create_buttons(self):
        for i in range(2):
            for j in range(2):
                idx = i * 2 + j
                b = tk.Button(
                    self.canvas,
                    text=self.btns[idx],
                    image=self.imgs[idx],
                    compound="top",
                    command=lambda n=self.btns[idx]: self.on_click(n)
                )
                x = 100 + j * 150
                y = 100 + i * 150
                self.canvas.create_window(x, y, window=b)
                b.bind("<Enter>", lambda e, i=idx: self.on_enter(e, i))
                b.bind("<Leave>", lambda e, i=idx: self.on_leave(e, i))
                self.button_list.append((b, idx))

    def on_click(self, name):
        mapping = {
            "Introduction": "intro",
            "About": "about",
            "Contact": "contact",
            "Exit": "exit"
        }
        self.open_notepad(mapping.get(name))

    def open_notepad(self, on):
        if on == "exit":
            self.root.quit()
            return

        nwd = tk.Toplevel(self.root)
        nwd.geometry("600x500")
        nwd.config(bg="Yellow")
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