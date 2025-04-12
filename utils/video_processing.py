import cv2
import numpy as np

def process_video(video_path, model, frame_interval=30, sequence_length=20, threshold=0.5):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    timestamps = []

    frames = []
    frame_num = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_num % frame_interval == 0:
            resized_frame = cv2.resize(frame, (64, 64))
            resized_frame = resized_frame / 255.0
            frames.append(resized_frame)

            if len(frames) == sequence_length:
                input_batch = np.expand_dims(frames, axis=0)  # shape: (1, 20, 64, 64, 3)
                prediction = model.predict(input_batch)[0][0]

                if prediction > threshold:
                    timestamps.append(int(frame_num / fps))
                
                frames = []  # reset frames for next batch

        frame_num += 1

    cap.release()
    return timestamps
