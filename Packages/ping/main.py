import sys
import requests
import time

try:
    from ping3 import ping
except ImportError:
    print("Установка зависимостей...")
    import subprocess
    subprocess.run("pip install ping3", shell=True)
    print("Перезапустите приложение после установки ping3.")
    sys.exit(1)


def main(argv: list[str], abspath: str):
    if len(argv) < 3:
        print("Использование:")
        print("  ping page <url> [-t]")
        print("  ping address <ip_or_host> [-t]")
        return 1

    mode = argv[1]
    target = argv[2]
    infinity = len(argv) > 3 and argv[3] == "-t"

    try:
        if mode == "page":
            while True:
                print(f"GET {target}...")
                try:
                    r = requests.get(target, timeout=5)
                    if r.status_code == 200:
                        print(f"OK 200 {target} {round(r.elapsed.total_seconds() * 1000)} мс")
                    else:
                        print(f"ERROR {r.status_code} {target} {round(r.elapsed.total_seconds() * 1000)} мс")
                except requests.RequestException as e:
                    print(f"Ошибка при запросе: {e}")

                if not infinity:
                    break
                time.sleep(1)

        elif mode == "address":
            while True:
                r = ping(target, timeout=4)
                if r is None:
                    print("Превышен интервал ожидания.")
                else:
                    print(f"Ответ от {target} спустя {round(r * 1000, 3)} мс")

                if not infinity:
                    break
                time.sleep(1)

        else:
            print("Неизвестная команда. Используйте 'page' или 'address'.")
            return 1

    except KeyboardInterrupt:
        print("Завершение по Ctrl+C.")
        return 0

    return 0