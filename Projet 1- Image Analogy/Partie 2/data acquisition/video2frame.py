import cv2
import os

video_path = 'Lina.mp4'

cap = cv2.VideoCapture(video_path)
all_frames = []

if not cap.isOpened():
    print("Error: Couldn't open the video.")
else:
    success, frame = cap.read()

    while success:
        # cv2.imwrite(f'frame{count}.jpg', frame)
        all_frames.append(frame)

        success, frame = cap.read()

    cap.release()

for i in range(len(all_frames)-1):
    cv2.imwrite(f'input3/framee{i}.jpg', all_frames[i])
    cv2.imwrite(f'target3/framee{i+1}.jpg', all_frames[i + 1])