import cv2
import numpy as np
import tflite_runtime.interpreter as tflite


interpreter = tflite.Interpreter(model_path="model_unquant.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

input_shape = input_details[0]['shape']  
input_size = input_shape[1]
input_dtype = input_details[0]['dtype']

labels = [line.strip().split(' ', 1)[1] for line in open("label.txt")]


cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Camera not detected — check `ls /dev/video*`")

ret, frame = cap.read()
cap.release()

if not ret:
    raise RuntimeError("Failed to capture frame")

cv2.imwrite("last_capture.jpg", frame)

img = cv2.resize(frame, (input_size, input_size))
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


img = img.astype(np.float32)
img = (img / 127.5) - 1.0
img = np.expand_dims(img, axis=0)


interpreter.set_tensor(input_details[0]['index'], img)
interpreter.invoke()
output = interpreter.get_tensor(output_details[0]['index'])[0]

predicted_index = int(np.argmax(output))
predicted_label = labels[predicted_index]
mold_probability = float(output[predicted_index])

print(f"Prediction: {predicted_label}")
print(f"Confidence: {mold_probability:.3f}")