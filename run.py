import marvin



cap = marvin.CameraCapture(0)
viewer = marvin.Cv2ImageViewer("test1")
writer = marvin.Cv2ImageWriter("/home/jeff/src/python/marvin/output/")

while 1:
    frame = cap.read()
    viewer.view(frame)
    writer.write(frame)
