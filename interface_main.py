import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.messagebox as msgbox

# Initialize the root Tkinter window
root = tk.Tk()
root.title("Тестирование солнечных панелей")

width = root.winfo_screenwidth()
height = root.winfo_screenheight()
# Открыть окно на весь экран
root.attributes('-fullscreen', True)


# Create the main layout frames
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=10, pady=10)

right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

# Create a table for the defects
labels = ["Количество дефектов", "Физические", "Электрические", "Загрязнение", "Скол"]
values = [1, 0, 0, 1, 0]

for i, (label, value) in enumerate(zip(labels, values)):
    tk.Label(left_frame, text=f"{label}:").grid(row=i, column=0, sticky='e')
    tk.Label(left_frame, text=str(value)).grid(row=i, column=1, sticky='w')

# Create a carousel frame for images (placeholder)
carousel_label = tk.Label(right_frame, text="Карусель изображений будет здесь")
carousel_label.pack()

# Create navigation buttons (placeholder actions)
button_prev = tk.Button(right_frame, text="<")
button_next = tk.Button(right_frame, text=">")
button_prev.pack(side=tk.LEFT)
button_next.pack(side=tk.RIGHT)

# Create a placeholder label for the graph
graph_label = tk.Label(root, text="График будет здесь")
graph_label.pack()

# Placeholder for a graph using matplotlib
dpi = 100  # DPI
width_in_inches = 900 / dpi  # Ширина в дюймах
height_in_inches = 700 / dpi  # Высота в дюймах

# Создать фигуру с заданными размерами
fig = plt.figure(figsize=(width_in_inches, height_in_inches), dpi=dpi)
ax = fig.add_subplot(111)

ax.plot(['10:00', '11:00', '12:00', '13:00'], [5, 10, 15, 20])
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea
canvas.draw()
canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


def on_closing():
    if msgbox.askokcancel("Выход", "Вы действительно хотите выйти?"):
        root.destroy()

# Привязка функции on_closing к событию закрытия окна
root.protocol("WM_DELETE_WINDOW", on_closing)


root.mainloop()
