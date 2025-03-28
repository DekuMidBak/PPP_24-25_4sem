# main.py
import socket
import os
import json
from datetime import datetime


def get_process_info():
    """Собирает информацию о запущенных процессах и форматирует в список."""
    process_list = []
    process_data = os.popen("ps aux").read().splitlines()
    headers = process_data[0].split()
    for line in process_data[1:]:
        parts = line.split(maxsplit=len(headers) - 1)
        process_list.append(dict(zip(headers, parts)))
    return process_list


def save_process_info():
    """Сохраняет информацию о процессах в файл JSON."""
    data = get_process_info()
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    filename = f"processes_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    return filename, data


def handle_client(client_socket):
    """Обрабатывает запросы клиента."""
    while True:
        command = client_socket.recv(1024).decode().strip()
        if not command:
            break

        response = {}

        if command == "update":
            filename, data = save_process_info()
            response = {
                "message": f"Process list saved in {filename}",
                "data": data
            }
            client_socket.sendall(json.dumps(response, indent=4).encode())

        elif command.startswith("kill "):
            try:
                parts = command.split()
                if len(parts) != 3:
                    raise ValueError(
                        "Invalid format. Use: kill <pid> <signal>"
                    )

                _, pid, sig = parts
                os.kill(int(pid), int(sig))
                response = {
                    "message": f"Process {pid} terminated with signal {sig}"
                }
            except ValueError as ve:
                response = {"error": str(ve)}
            except ProcessLookupError:
                response = {"error": f"No such process: {pid}"}
            except Exception as e:
                response = {"error": str(e)}

            client_socket.sendall(json.dumps(response, indent=4).encode())
            response.clear()
            client_socket.close()
            return

        else:
            response = {"error": "Invalid command"}
            client_socket.sendall(json.dumps(response, indent=4).encode())


def main():
    """Запускает сервер."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 1234))
    server.listen(5)
    print("[SERVER] Listening on port 1234...")

    while True:
        client_socket, addr = server.accept()
        print(f"[SERVER] Connection from {addr}")
        handle_client(client_socket)
        client_socket.close()


if __name__ == "__main__":
    main()
