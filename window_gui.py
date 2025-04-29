import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import ImageTk, Image


# Setup Window
wd = tk.Tk()
wd.title("Welcome to IR's Window GUI")
wd.geometry("400x300")

# Load original image once
original_bg = Image.open("F:/Python/1. WINDOW GUI/IMAGES/IR x ST.png")

# Create a Canvas instead of Label
canvas = tk.Canvas(wd, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Load original image once
original_bg = Image.open("F:/Python/1. WINDOW GUI/IMAGES/IR x ST.png")

# Create a dummy image initially (will be replaced shortly)
dummy_img = ImageTk.PhotoImage(Image.new("RGB", (1, 1)))
bg_item = canvas.create_image(0, 0, anchor="nw", image=dummy_img)
canvas.image = dummy_img

# Resize the image based on window size
def resize_bg(event=None):
    new_w = wd.winfo_width()
    new_h = wd.winfo_height()
    resized = original_bg.resize((new_w, new_h), Image.LANCZOS)
    new_bg = ImageTk.PhotoImage(resized)
    canvas.itemconfig(bg_item, image=new_bg)
    canvas.image = new_bg  # Save reference

# Bind resize event
wd.bind("<Configure>", resize_bg)

# Call it once after window is initialized
wd.after(100, resize_bg)

# Load original images for buttons
original_imgs = [
    Image.open("F:/Python/1. WINDOW GUI/IMAGES/Information icon.png"),
    Image.open("F:/Python/1. WINDOW GUI/IMAGES/About icon.png"),
    Image.open("F:/Python/1. WINDOW GUI/IMAGES/Contact icon.png"),
    Image.open("F:/Python/1. WINDOW GUI/IMAGES/Exit icon.png"),
]

# Make small 50x50 versions for starting
imgs = [ImageTk.PhotoImage(img.resize((50, 50))) for img in original_imgs]

btns = ["Introduction", "About", "Contact", "Exit"]

# Make a Notepad
def open_notepad(on):
    nwd = tk.Toplevel(wd)
    nwd.geometry("600x500")
    nwd.config(bg="Yellow")
    nwd.resizable(10, 10)
    frame = tk.Frame(nwd)
    frame.pack(fill="both", expand=True)
    txt = tk.Text(frame, width=50, height=20, wrap="word", font=("Consolas", 12))
    
    if on == "intro":
        nwd.title("IR.Introduction")
        intro_cont = """
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

    Thank you for checking out this project! 🎉"""
        txt.insert(tk.END, intro_cont)
    
    elif on == "about":
        nwd.title("IR.About")
        about_cont = """
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

Keep exploring and building! 🚀"""
        txt.insert(tk.END, about_cont)
    
    elif on == "contact":
        nwd.title("IR.Contact")
        contact_cont = """
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
        txt.insert(tk.END, contact_cont)
    
    else:
        nwd.title("IR.Exit")
        wd.quit()
    
    txt.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    scrollbar = tk.Scrollbar(frame, command=txt.yview)
    scrollbar.pack(side="right", fill="y")
    txt.config(yscrollcommand=scrollbar.set)
    txt.config(state="disabled")
    nwd.mainloop()


# Create Buttons with Images
def on_click(name):
    if name == "Introduction":
        open_notepad("intro")
    elif name == "About":
        open_notepad("about")
    elif name == "Contact":
        open_notepad("contact")
    elif name == "Exit":
        wd.quit()

# -- inside your loop:
button_list = []

for i in range(2):
    for j in range(2):
        idx = i * 2 + j
        b = tk.Button(canvas, text=btns[idx], image=imgs[idx % 4], compound="top", command=lambda n=btns[idx % 4]: on_click(n))
        x = 100 + j * 150
        y = 100 + i * 150
        canvas.create_window(x, y, window=b)
        button_list.append((b, idx))



hovering = {}  # To track which button is hovered

def animate_resize(widget, idx, grow=True, step=0):
    if not hovering.get(widget, False) and grow:
        return
    if hovering.get(widget, False) and not grow:
        return

    base_size = 50
    max_size = 55
    size_step = 2

    if grow:
        new_size = base_size + step * size_step
        if new_size >= max_size:
            new_size = max_size
    else:
        new_size = max_size - step * size_step
        if new_size <= base_size:
            new_size = base_size

    # --- Correct image resizing:
    resized_img = original_imgs[idx].resize((new_size, new_size), Image.LANCZOS)
    tk_img = ImageTk.PhotoImage(resized_img)
    widget.config(image=tk_img)
    widget.image = tk_img

    if (grow and new_size < max_size) or (not grow and new_size > base_size):
        widget.after(30, animate_resize, widget, idx, grow, step + 1)

def on_enter(event, idx):
    hovering[event.widget] = True
    event.widget.config(bg="lightblue")
    animate_resize(event.widget, idx, grow=True)

def on_leave(event, idx):
    hovering[event.widget] = False
    event.widget.config(bg="SystemButtonFace")
    animate_resize(event.widget, idx, grow=False)


for btn, idx in button_list:
    btn.bind("<Enter>", lambda e, i=idx: on_enter(e, i))
    btn.bind("<Leave>", lambda e, i=idx: on_leave(e, i))


wd.mainloop()
