import socket
import threading
from gpiozero import AngularServo
from time import sleep
from picamzero import Camera
import io
import os

def move_servo(steps):
    servo = AngularServo(18, min_angle=0, max_angle=360, min_pulse_width=0.0007, max_pulse_width=0.0023)
    for _ in range(steps):
        servo.min()
        sleep(0.1035)
        servo.mid()

def take_image(image_name="test.jpg"):
    cam = Camera()
    cam.start_preview()
    sleep(2)
    cam.take_photo(image_name)
    return image_name

def handle_client(conn):
    try:
        while True:
            command = conn.recv(1024).decode().strip()
            if not command:
                break
            print(f"Received: {command}")

            if command.startswith("take_image"):
                _, filename = command.split()
                take_image(filename)
                with open(filename, 'rb') as f:
                    img = f.read()
                conn.sendall(len(img).to_bytes(4, 'big'))
                conn.sendall(img)
                os.remove(filename)

            elif command.startswith("move_servo"):
                _, steps = command.split()
                move_servo(int(steps))
                conn.sendall(b"done")

            elif command == "exit":
                break
    finally:
        conn.close()

def start_server(host='0.0.0.0', port=9000):
    with socket.socket() as s:
        s.bind((host, port))
        s.listen(1)
        print(f"Listening on {host}:{port}")
        while True:
            conn, addr = s.accept()
            print(f"Connected: {addr}")
            threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

if __name__ == "__main__":
    start_server()
