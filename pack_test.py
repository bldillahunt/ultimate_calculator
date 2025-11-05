import tkinter as tk

root = tk.Tk()
root.title("Tkinter Pack Example")

label1 = tk.Label(root, text="Label 1", bg="lightblue")
label2 = tk.Label(root, text="Label 2", bg="lightgreen")
label3 = tk.Label(root, text="Label 3", bg="lightcoral")

# Pack widgets
label1.pack(side="top", fill="x", padx=5, pady=5)
label2.pack(side="left", padx=5, pady=5)
label3.pack(side="right", padx=5, pady=5)

root.mainloop()