import cv2
import numpy as np
import time
import tflite_runtime.interpreter as tflite

interpreter = tflite.Interpreter(model_path="model_unquant.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


print("Input details:", input_details)
print("Output details:", output_details)

input_shape = input_details[0]['shape']
input_size = input_shape[1]
input_dtype = input_details[0]['dtype']

labels = [line.strip().split(' ', 1)[1] for line in open("label.txt")]


cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
time.sleep(2)  

for _ in range(5):
    cap.read()  

ret, frame = cap.read()
cap.release()

if not ret:
    raise RuntimeError("Failed to capture frame — check camera connection with `ls /dev/video*`")

cv2.imwrite("last_capture.jpg", frame)  


img = cv2.resize(frame, (input_size, input_size))
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

input_scale, input_zero_point = input_details[0]['quantization']

if input_dtype == np.uint8:
    
    img = img.astype(np.uint8)
elif input_dtype == np.int8:
    if input_scale != 0:
        img = (img.astype(np.float32) / input_scale + input_zero_point).astype(np.int8)
    else:
        img = img.astype(np.int8)
else:
    
    img = img.astype(np.float32)
    img = (img / 127.5) - 1.0

img = np.expand_dims(img, axis=0)

# --- Run inference ---
interpreter.set_tensor(input_details[0]['index'], img)
interpreter.invoke()
output = interpreter.get_tensor(output_details[0]['index'])[0]

# --- Correctly dequantize OUTPUT (independent of input dtype) ---
output_dtype = output_details[0]['dtype']
output_scale, output_zero_point = output_details[0]['quantization']

if output_dtype in (np.uint8, np.int8) and output_scale != 0:
    probs = (output.astype(np.float32) - output_zero_point) * output_scale
else:
    probs = output.astype(np.float32)

# --- Interpret result ---
predicted_index = int(np.argmax(probs))
predicted_label = labels[predicted_index]
mold_probability = float(probs[predicted_index])

print(f"Prediction: {predicted_label}")
print(f"Confidence: {mold_probability:.3f}")