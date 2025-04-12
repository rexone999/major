
import cv2
import numpy as np

def process_video(video_path, model, frame_interval=30, threshold=0.5):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    timestamps = []

    frame_num = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_num % frame_interval == 0:
            resized_frame = cv2.resize(frame, (64, 64))
            resized_frame = resized_frame / 255.0
            resized_frame = np.expand_dims(resized_frame, axis=0)
            prediction = model.predict(resized_frame)[0][0]

            if prediction > threshold:
                timestamps.append(int(frame_num / fps))

        frame_num += 1

    cap.release()
    return timestamps
