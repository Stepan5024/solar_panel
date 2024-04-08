from ultralytics import YOLO

# Загрузите обученную модель
model = YOLO("path/to/best.pt")  # Замените путь на фактический путь к вашему файлу модели

# Экспорт в ONNX
model.export("model.onnx")