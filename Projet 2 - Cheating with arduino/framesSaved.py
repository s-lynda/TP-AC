import cv2


# Function to save frames
def save_frames(video_capture, output_folder):
    frame_count = 0

    while True:
        ret, frame = video_capture.read()

        if not ret:
            break

        frame_count += 1
        frame_filename = f"{output_folder}/frame_{frame_count:04d}.jpg"
        cv2.imwrite(frame_filename, frame)

        cv2.imshow("Video", frame)

        key = cv2.waitKey(1)

        # Check if 'q' key is pressed to quit the program
        if key == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


# Video file path
video_path = "20231114_114750.mp4"

# Output folder for saved frames
output_folder = "Frames"

# Open the video file
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Unable to open video file.")
    exit()

# Create the output folder if it doesn't exist
import os

os.makedirs(output_folder, exist_ok=True)

# Start saving frames
save_frames(cap, output_folder)
