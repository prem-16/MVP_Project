import socket

RASPI_IP = '192.168.0.20'  # Or use IP like '192.168.1.10'
PORT = 9000

def send_command(command, expect_image=False, save_as="received.jpg"):
    sock = socket.socket()
    sock.connect((RASPI_IP, PORT))
    sock.sendall(command.encode())

    if expect_image:
        img_len_bytes = sock.recv(4)
        img_len = int.from_bytes(img_len_bytes, 'big')
        data = b''
        while len(data) < img_len:
            packet = sock.recv(4096)
            if not packet:
                break
            data += packet
        with open(save_as, 'wb') as f:
            f.write(data)
        print(f"Image saved as {save_as}")
    else:
        response = sock.recv(1024)
        print("Response:", response.decode())

    sock.close()

# Example usage
send_command("take_image test1.jpg", expect_image=True)
send_command("move_servo 1")
