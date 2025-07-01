import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

MAX_THREADS = 500
TIMEOUT_TCP = 0.3
TIMEOUT_UDP = 0.5

open_tcp = []
open_udp = []

lock = threading.Lock()

def scan_tcp(ip: str, port: int):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT_TCP)
            if s.connect_ex((ip, port)) == 0:
                with lock:
                    open_tcp.append(port)
    except:
        pass

def scan_udp(ip: str, port: int):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(TIMEOUT_UDP)
            s.sendto(b'', (ip, port))
            s.recvfrom(1024)
            with lock:
                open_udp.append(port)
    except socket.timeout:
        # UDP порты могут молчать даже если открыты
        with lock:
            open_udp.append(port)
    except:
        pass

def main(argv: list[str]):
    if len(argv) < 2:
        print("Использование: portscan <хост или IP>")
        return 1
    prompt = input("Сканировать UPD порты?")
    if prompt.lower() in ["y", "д"]:
        scanning_udp = True
    else:
        scanning_udp = False
    target = argv[1].strip()
    try:
        ip = socket.gethostbyname(target)
    except:
        print("Ошибка: не удалось разрешить хост.")
        return 1

    print(f"Сканирую {ip} на открытые порты TCP...")

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        for port in range(1, 65535):  # можно увеличить до 65535
            executor.submit(scan_tcp, ip, port)
    if scanning_udp:
        print(f"Сканирую {ip} на открытые или откликающиеся порты UDP...")

        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            for port in range(1, 1025):  # UDP >1024 часто бесполезны
                executor.submit(scan_udp, ip, port)
        print("\nUDP-порты (возможно открыты или не ответили):")
        if open_udp:
            for p in sorted(open_udp):
                print(f"  {p}")
        else:
            print("Нет UDP портов, которые ответили или проигнорировали.")

    # Вывод
    print("\nОткрытые TCP-порты:")
    if open_tcp:
        for p in sorted(open_tcp):
            print(f"  {p}")
    else:
        print("Нет открытых TCP портов.")


    return 0