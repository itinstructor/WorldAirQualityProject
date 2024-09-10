import tkinter as tk
from tkinter import font


def main():
    root = tk.Tk()
    root.title("Default Font Display")
    root.geometry("300x100")

    # Get the default font
    default_font = font.nametofont("TkDefaultFont")
    font_name = default_font.actual()["family"]
    font_size = default_font.actual()["size"]

    # Create and pack a label with the default font information
    label = tk.Label(root, text=f"Default Font: {font_name}\nSize: {font_size}")
    label.pack(expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()
