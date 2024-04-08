from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.yaml")  # build a new model from scratch

# Use the model
results = model.train(data="config.yaml", epochs=100)  # train the model
#model.val()  # оцените производительность модели на наборе проверки
