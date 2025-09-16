import cv2
import socket
import numpy as np

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 9999))
buffer = b""

while True:
    packet, _ = sock.recvfrom(65536)
    marker, data = packet[:1], packet[1:]
    buffer += data
    if marker == b'1':
        frame = cv2.imdecode(np.frombuffer(buffer, dtype=np.uint8), 1)
        if frame is not None:
            cv2.imshow("Video", frame)
        buffer = b""
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
sock.close()

