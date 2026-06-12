import cv2
import serial
import time
from ultralytics import YOLO

SERIAL_PORT = '/dev/cu.usbmodemXXXX' 
BAUD_RATE = 9600

TARGET_CLASS = 67 

try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to Arduino on {SERIAL_PORT}")
    time.sleep(2) # CRITICAL: Wait for Arduino bootloader to finish resetting
except Exception as e:
    print(f"Serial Error: {e}")
    exit()

print("Loading YOLOv8n model...")
model = YOLO('yolov8n.pt')

cap = cv2.VideoCapture(0)
print("Vision pipeline active. Show your phone to the camera. Press 'q' to quit.")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Run YOLO inference on the current frame
        results = model(frame, stream=True, verbose=False)
        target_detected = False

        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Check if the detected object matches our target class
                if int(box.cls[0]) == TARGET_CLASS:
                    target_detected = True
                    
                    # Draw a bounding box for visual feedback
                    x1, y1, x2, y2 = box.xyxy[0]
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    cv2.putText(frame, "TARGET ACQUIRED -> LED ON", (int(x1), int(y1)-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # 4. Trigger the Hardware
        if target_detected:
            arduino.write(b'1')
        else:
            arduino.write(b'0')

        # Display the live feed
        cv2.imshow('YOLO Serial Trigger', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\nProcess interrupted.")

finally:
    arduino.write(b'0')
    arduino.close()
    cap.release()
    cv2.destroyAllWindows()
    print("Shutdown complete.")

