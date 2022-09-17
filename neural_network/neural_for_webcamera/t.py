from vidgear.gears import CamGear
import cv2

URL = "https://www.youtube.com/watch?v=AxnSU3YgnU0&ab_channel=FalconTravel"
stream = CamGear(source=URL, stream_mode=True).start()  

while True:
    frame = stream.read()
    if frame is None:
        break
    frame = cv2.resize(frame, (1080, 600))
    cv2.imshow("Output Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()
stream.stop()
