import os
from ultralytics import YOLO
import cv2
import cv2

# Получаем информацию о сборке OpenCV
build_info = cv2.getBuildInformation()

# Ищем информацию о поддерживаемых кодеках
codec_info = build_info[build_info.find("Video I/O:"):]

print("Поддерживаемые кодеки:")
print(codec_info)

VIDEOS_DIR = os.path.join('F:\\', 'solar_panel')

video_path = os.path.join(VIDEOS_DIR, 'test_video1.mp4')
video_path_out = '{}_out.mp4'.format(video_path)
print(f"video_path {video_path}")
cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()

if ret:  # Check if video is successfully read
    H, W, _ = frame.shape
    out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

    model_path = os.path.join('F:\\', 'solar_panel', 'runs', 'detect', 
                              'train3', 'weights', 'best.pt')

    # Load a model
    model = YOLO(model_path)  # load a custom model

    threshold = 0.5

    while ret:
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
else:
    print("Error: Failed to read video.")
