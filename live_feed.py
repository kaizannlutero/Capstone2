from picamera2 import Picamera2
import cv2

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (1280, 720)}))
picam2.start()

while True:
    frame = picam2.capture_array()
    cv2.imshow("HQ Camera Feed", frame)

    key = cv2.waitKey(1) & 0xFF

    # PRESS Q TO EXIT PROPERLY
    if key == ord('q'):
        break

picam2.stop()
cv2.destroyAllWindows()
