import socket
import threading

open_tcp = []
open_udp = []

def scan_tcp(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.3)
            if s.connect_ex((ip, port)) == 0:
                open_tcp.append(port)
    except:
        pass

def scan_udp(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(0.5)
            s.sendto(b'', (ip, port))
            s.recvfrom(1024)  # Попытка получить ответ
            open_udp.append(port)
    except socket.timeout:
        open_udp.append(port)  # Нет ответа — UDP может быть открыт
    except:
        pass

def main(argv:list[str]):
    target = argv[1].strip()

    try:
        ip = socket.gethostbyname(target)
    except:
        print("Ошибка: не удалось разрешить хост.")
        return 1

    print(f"Сканирую {ip} на открытые порты TCP/UDP...")

    threads = []
    for port in range(1, 65536):
        t = threading.Thread(target=scan_tcp, args=(ip, port))
        threads.append(t); t.start()
    for t in threads: t.join()

    threads = []
    for port in range(1, 65536):
        t = threading.Thread(target=scan_udp, args=(ip, port))
        threads.append(t); t.start()
    for t in threads: t.join()

    print("\n📡 Открытые TCP-порты:")
    for p in sorted(open_tcp): print(f"  {p}")

    print("\n📡 Открытые или неотвечающие UDP-порты:")
    for p in sorted(open_udp): print(f"  {p}")

    return 0
