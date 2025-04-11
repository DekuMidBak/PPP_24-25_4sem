# client.py
import socket
import json


# asdasdasdasdasdasd
def start_client():
    """Запускает клиент и позволяет взаимодействовать с сервером."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 1234))

    while True:
        command = input(
            "Enter command (update / kill <pid> <signal> / exit): "
            )
        if command == "exit":
            break
        client.sendall(command.encode())
        response = client.recv(1024).decode()

        try:
            response_data = json.loads(response)
            print(json.dumps(response_data, indent=4, ensure_ascii=False))
        except json.JSONDecodeError:
            print("[SERVER RESPONSE]:\n", response)

    client.close()


if __name__ == "__main__":
    start_client()
