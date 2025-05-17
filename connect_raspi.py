import socket

RASPI_IP = '192.168.0.20'  # Or use IP like '192.168.1.10'
PORT = 9000
from time import sleep

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


def get_image(command, expect_image=False, save_as="received.jpg"):
    sock = socket.socket()
    sock.connect((RASPI_IP, PORT))
    sock.sendall(command.encode())
    data = b''
    if expect_image:
        img_len_bytes = sock.recv(4)
        img_len = int.from_bytes(img_len_bytes, 'big')
        
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
    return save_as
    
   

# Example usage


if __name__ == "__main__":
    imageNumber="mirror_test"

    send_command("take_image test_image_FGS580.jpg", expect_image=True, save_as=f"test_image_{imageNumber}_FGS580.jpg") # FGS580
    send_command("move_servo 1")
    sleep(2)
    send_command("take_image test_image_FGUV.jpg", expect_image=True, save_as = f"test_image_{imageNumber}_FGUV.jpg")
    send_command("move_servo 1")
    sleep(2)
    send_command("take_image test_image_FGL850.jpg", expect_image=True, save_as = f"test_image_{imageNumber}_FGL850.jpg")
    send_command("move_servo 1")
    sleep(2)
    send_command("take_image test_image_FG37.jpg", expect_image=True, save_as = f"test_image_{imageNumber}_FG37.jpg")
    send_command("move_servo 1")
    sleep(2)
    send_command("move_servo 1")
    sleep(2)
    send_command("take_image test_image_FG1000.jpg", expect_image=True, save_as =f"test_image_{imageNumber}_FG1000.jpg")
    send_command("move_servo 1")
    sleep(2)





