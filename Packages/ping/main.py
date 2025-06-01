import requests
import time

def format_time(seconds: float) -> str:
    return f"{round(seconds * 1000, 1)} мс" if seconds < 1 else f"{round(seconds, 2)} с"

def ensure_scheme(url: str) -> str:
    if not url.startswith("http://") and not url.startswith("https://"):
        return "https://" + url
    return url

def main(argv: list[str], abspath: str):
    try:
        from ping3 import ping
    except ImportError:
        print("Установка зависимостей...")
        import subprocess
        subprocess.run("pip install ping3", shell=True, capture_output=False)
        print("Перезапустите приложение!")
        return 1

    if len(argv) < 3:
        print("Передайте команду и адрес в аргументы!")
        print("ping page|address <адрес> [-t]")
        return 1

    command = argv[1]
    target = argv[2]
    infinity = "-t" in argv

    try:
        if command == "page":
            target = ensure_scheme(target)
            while True:
                print(f"GET {target}...")
                try:
                    start = time.time()
                    r = requests.get(target, timeout=5)
                    end = time.time()
                    elapsed = end - start

                    status = f"OK {r.status_code}" if r.status_code == 200 else f"ERROR {r.status_code}"
                    print(f"{status} {target} {format_time(elapsed)}")
                except requests.RequestException as e:
                    print(f"Ошибка при запросе: {e}")
                if not infinity:
                    break
                time.sleep(1)

        elif command == "address":
            while True:
                r = ping(target, timeout=4)
                if r is None:
                    print("Превышен интервал ожидания")
                else:
                    print(f"Ответ от {target} спустя {format_time(r)}")
                if not infinity:
                    break
                time.sleep(1)

        else:
            print("Неизвестная команда. Используйте 'page' или 'address'")
            return 1

    except KeyboardInterrupt:
        print("Завершение по Ctrl+C.")
        return 0
