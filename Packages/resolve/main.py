import socket

def main(argv:list[str]):
    try:
        if len(argv) < 2:
            print("Передайте домен в аргументы!")
            return 1
        ip = socket.gethostbyname(argv[1])
        print(f"IP для {argv[1]}: {ip}")
        return 0
    except socket.gaierror:
        print("Не удалось получить IP адрес")
        return 1