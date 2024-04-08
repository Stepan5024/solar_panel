import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
# Импорт модуля font для настройки шрифтов
from tkinter import font as tkFont
from PIL import Image, ImageTk
import cv2
from tkinter import filedialog
from ultralytics import YOLO
import os
import threading


# Загружаем модель YOLO
model_path = os.path.join('F:\\', 'solar_panel', 'runs', 'detect', 
                              'train3', 'weights', 'best.pt')
model = YOLO(model_path)  # Загрузка модели YOLO
threshold = 0.5  # Порог для обнаружения


def analyze_video(video_path, video_path_out, model, threshold):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Ошибка при открытии видео файла.")
        return

    ret, frame = cap.read()
    if ret:
        H, W, _ = frame.shape
        out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

        while ret:
            # Применяем модель YOLO к кадру
            results = model(frame)[0]

            for result in results.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = result
                if score > threshold:
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
                    cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

            out.write(frame)
            ret, frame = cap.read()

        cap.release()
        out.release()
        cv2.destroyAllWindows()
        print("Анализ видео завершен, результат сохранен как:", video_path_out)
    else:
        print("Ошибка: не удалось прочитать видео.")


# Функция, вызываемая при нажатии на кнопку загрузки видео
def load_video():
    # Открываем диалоговое окно для выбора файла
    video_path = filedialog.askopenfilename(title="Выберите видео файл", 
                                            filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*")))
    if not video_path:  # Проверка на случай отмены выбора файла
        return
    
    
    video_path_out = f"{video_path.split('.')[0]}_out.mp4"
    
    # Запуск длительной операции в отдельном потоке
    thread = threading.Thread(target=analyze_video, args=(video_path, video_path_out, model, threshold))
    thread.start()


# Функция для обновления изображения в карусели
def update_image(step):
    global current_image_index, images, image_label, index_label
    current_image_index = (current_image_index + step) % len(images)
    image_label.configure(image=images[current_image_index])
    
    # Обновление метки индекса
    index_label.configure(text=f"{current_image_index + 1} / {len(images)}")

# Функция для обновления изображения в карусели после удаления
def update_carousel():
    global current_image_index, images, image_label, index_label
    if not images:  # Если массив изображений пуст, обновляем метку
        index_label.configure(text="Нет изображений")
        image_label.configure(image=None)
        return
    if current_image_index >= len(images):  # Если индекс за пределами, обновляем на последний
        current_image_index = len(images) - 1
    image_label.configure(image=images[current_image_index])
    index_label.configure(text=f"{current_image_index + 1} / {len(images)}")

# Функция для удаления текущего изображения
def confirm_deletion():
    global current_image_index, images
    if images and 0 <= current_image_index < len(images):
        del images[current_image_index]  # Удаляем изображение
        update_carousel()  # Обновляем карусель    

# Функция для создания изображения Tkinter из файла
def create_image(file_path):
    image = Image.open(file_path)
    image.thumbnail((300, 300))  # Предположим, что мы хотим максимальную ширину и высоту в 300 пикселей
    return ImageTk.PhotoImage(image)

# Функция для создания изображения Tkinter из файла
def create_image(file_path):
    image = Image.open(file_path)
    image.thumbnail((300, 300))  # Предположим, что мы хотим максимальную ширину и высоту в 300 пикселей
    return ImageTk.PhotoImage(image)

# Create the main window
root = tk.Tk()
root.title("Система контроля качества")
root.state('zoomed')  # Maximize the window while keeping window controls visible
# Создание шрифта
customFont = tkFont.Font(family="Helvetica", size=18)

# Create a central frame to hold all other widgets
central_frame = tk.Frame(root)
central_frame.pack(expand=True, fill='both')

# Define the data for the defects table
defects_data = {
    "Количество дефектов": 1,
    "Физические": 0,
    "Электрические": 0,
    "Загрязнение": 1,
    "Скол": 0
}

# Create the table
table_frame = ttk.Frame(central_frame)
table_frame.pack(side='left', expand=True, padx=50, pady=50)

for i, (label, value) in enumerate(defects_data.items()):
    tk.Label(table_frame, text=label, font=customFont).grid(row=i, column=0, sticky='w')
    tk.Label(table_frame, text=value, font=customFont).grid(row=i, column=1, sticky='e')

# Предположим, что у вас есть список путей к файлам изображений
image_paths = ['./images/image1.jpg', './images/image2.jpg']  # Замените на реальные пути к файлам
images = [create_image(path) for path in image_paths]  # Создать изображения Tkinter
current_image_index = 0  # Индекс текущего изображения в карусели


# Create carousel frame
carousel_frame = ttk.Frame(central_frame)
carousel_frame.pack(side='right', 
                    expand=True, padx=50, pady=50)
# Placeholder for the image carousel
carousel_placeholder = tk.Label(carousel_frame, 
                                font=customFont,  
                                text="Проверено солнечных панелей – 20 шт")
carousel_placeholder.pack()
# Label for the carousel
carousel_label = tk.Label(carousel_frame, 
                          font=customFont, 
                          text="Требует перепроверки: 2")
carousel_label.pack()

# Создаем кнопку для загрузки видео файла
load_video_button = tk.Button(root, 
                              text="Загрузить видео", 
                              command=load_video)
load_video_button.pack()

# Метка для отображения изображения
image_label = tk.Label(carousel_frame, 
                       image=images[current_image_index])
image_label.pack()
# Создаем выпадающий список с выбором дефектов
defect_types = ["Физическое", "Электрическое", "Загрязнение", "Скол"]
defects_combobox = ttk.Combobox(carousel_frame, values=defect_types, state="readonly")
defects_combobox.pack(side=tk.BOTTOM, pady=5)
defects_combobox.set(defect_types[0])  # Устанавливаем значение по умолчанию


# Create navigation buttons (placeholder actions)
# Кнопки навигации
button_prev = tk.Button(carousel_frame, text="<", 
                        command=lambda: update_image(-1))
button_next = tk.Button(carousel_frame, text=">", 
                        command=lambda: update_image(1))
button_prev.pack(side=tk.LEFT)
button_next.pack(side=tk.RIGHT)

# Создаем кнопку "Подтвердить" для удаления изображения
confirm_button = tk.Button(carousel_frame, 
                           text="Подтвердить", 
                           command=confirm_deletion)
confirm_button.pack(side=tk.BOTTOM, pady=10)
# Метка для отображения текущего индекса изображения
index_label = tk.Label(carousel_frame, font=customFont, text=f"1 / {len(images)}")
index_label.pack(side=tk.TOP, pady=10)  # Размещение над кнопками



# Create the graph below the table and carousel
figure = Figure(figsize=(5, 4), dpi=100)
subplot = figure.add_subplot(111)
# Simulate some data
times = ['10:00', '11:00', '12:00']
values = np.cumsum(np.random.rand(3) * 10).tolist()
subplot.plot(times, values)
subplot.set_title("Количество распознанных солнечных панелей")
subplot.set_xlabel("Время")
subplot.set_ylabel("Количество, шт")

canvas = FigureCanvasTkAgg(figure, master=central_frame)
canvas.draw()
canvas.get_tk_widget().pack(side='bottom', expand=True, padx=50, pady=50)

# Start the Tkinter event loop
root.mainloop()
