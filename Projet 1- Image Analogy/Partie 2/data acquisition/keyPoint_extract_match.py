import cv2 as cv
import numpy as np

net = cv.dnn.readNetFromTensorflow('graph_opt.pb')

inWidth = 368
inHeight = 368
thr = 0.2

BODY_PARTS = {"Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
              "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
              "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
              "LEye": 15, "REar": 16, "LEar": 17, "Background": 18}

POSE_PAIRS = [["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
              ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
              ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
              ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
              ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"]]


def estimatePose(frame):
    frameWidth, frameHeight = frame.shape[1], frame.shape[0]

    net.setInput(cv.dnn.blobFromImage(frame, 0.1, (inWidth, inHeight), (127.5, 127.5, 127.5), swapRB=True, crop=False))
    out = net.forward()

    assert (len(BODY_PARTS) <= out.shape[1])

    points = []
    for i in range(len(BODY_PARTS)):
        # Slice heatmap of corresponding body's part.
        heatMap = out[0, i, :, :]

        # Originally, we try to find all the local maximums. To simplify a sample
        # we just find a global one. However only a single pose at the same time
        # could be detected this way.
        _, conf, _, point = cv.minMaxLoc(heatMap)
        x = (frameWidth * point[0]) / out.shape[3]
        y = (frameHeight * point[1]) / out.shape[2]

        # Add a point if it's confidence is higher than threshold.
        points.append((int(x), int(y)) if conf > thr else None)

    for pair in POSE_PAIRS:
        partFrom = pair[0]
        partTo = pair[1]
        assert (partFrom in BODY_PARTS)
        assert (partTo in BODY_PARTS)

        idFrom = BODY_PARTS[partFrom]
        idTo = BODY_PARTS[partTo]

        if points[idFrom] and points[idTo]:
            cv.line(frame, points[idFrom], points[idTo], (0, 0, 255), 3)
            cv.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (0, 255, 0), cv.FILLED)
            cv.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (0, 255, 0), cv.FILLED)

    t, _ = net.getPerfProfile()
    freq = cv.getTickFrequency() / 1000
    cv.putText(frame, '%.2fms' % (t / freq), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

    return frame, points


video1_path = 'Linda.mp4'
cap = cv.VideoCapture(video1_path)

video2_path = 'Lina.mp4'
cap2 = cv.VideoCapture(video2_path)

count = 0

while True:
    ret, frame = cap.read()
    ret2, frame2 = cap2.read()
    count += 1

    if ret and ret2:
        frame, points = estimatePose(frame)
        frame2, points2 = estimatePose(frame2)

        for pair in POSE_PAIRS:
            partFrom = pair[0]
            partTo = pair[1]
            assert (partFrom in BODY_PARTS)
            assert (partTo in BODY_PARTS)

            idFrom = BODY_PARTS[partFrom]
            idTo = BODY_PARTS[partTo]
        
            if points[idFrom] and points[idTo]:
                cv.line(frame2, points[idFrom], points[idTo], (0, 255, 0), 3)
                cv.ellipse(frame2, points[idFrom], (3, 3), 0, 0, 360, (0, 255, 0), cv.FILLED)
                cv.ellipse(frame2, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)

            if points2[idFrom] and points2[idTo]:
                cv.line(frame2, points2[idFrom], points2[idTo], (0, 0, 255), 3)  # Green lines for the second video
                cv.ellipse(frame2, points2[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)  # Green ellipses
                cv.ellipse(frame2, points2[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)  # Green ellipses

        cv.imwrite(f'results4/frame{count}.jpg', frame2)
        cv.imshow('Capture', frame)
        cv.imshow('Capture2', frame2)

    else:
        break

    k = cv.waitKey(1)
    if k & 0xFF == ord("q"):  # Exit condition
        break

cap.release()
cap2.release()
cv.destroyAllWindows()

        
  


