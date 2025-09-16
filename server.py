import cv2
import socket
import numpy as np
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = ("127.0.0.1", 9999)
cap = cv2.VideoCapture("video.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
interval = 1 / fps if fps > 0 else 0.03

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (640, 480))
    encoded, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
    data = buffer.tobytes()
    size = 60000
    for i in range(0, len(data), size):
        chunk = data[i:i+size]
        marker = b'1' if i+size >= len(data) else b'0'
        sock.sendto(marker + chunk, server_addr)
    time.sleep(interval)

cap.release()
sock.close()

